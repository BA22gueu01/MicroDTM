import OpenSSL
import logging
import requests
import socket
import ssl
import subprocess
import time

PROMETHEUS = 'http://10.161.2.161:31090/'
PARAMETERWEIGHT = 0.2

KEYS = ["uptime", "counter_status_200_carts_customerId_items", "gauge_response_metrics", "container_spec_cpu_quota"]
parameterQueriesToValues = {k:None for k in KEYS}
#parameterQueriesToValues = {k:[20, 10] for k in KEYS}

def trustCalculation(parameterGradeList):
    trustScore = 0

    for x in range(len(parameterGradeList)):
        trustScore = trustScore + (parameterGradeList[x] * PARAMETERWEIGHT)

    print("Trustscore: ", trustScore)


def availabilityGradeCalculation(uptimeGrade):
    uptimeWeight = 1
    return uptimeWeight * uptimeGrade


def reliabilityGradeCalculation(responseErrorsGrade, logLevelGrade):
    responseErrorsWeight = 0.4
    logLevelWeight = 0.6
    return (responseErrorsWeight * responseErrorsGrade) + (logLevelWeight * logLevelGrade)


def performanceGradeCalculation(responseTimeGrade, throughputGrade, cpuUsageGrade):
    responseTimeWeight = 0.5
    throughputWeight = 0.3
    cpuUsageWeight = 0.2
    return (responseTimeWeight * responseTimeGrade) + (throughputWeight * throughputGrade) + (
                cpuUsageWeight * cpuUsageGrade)


def correctnessGradeCalculation(numberOfCorrectCallsGrade):
    numberOfCorrectCallsWeight = 1.0
    return numberOfCorrectCallsWeight * numberOfCorrectCallsGrade


def securityGradeCalculation(secureChannelWeightGrade, apparmorGrade, certificateGrade):
    secureChannelWeight = 0.7
    apparmorWeight = 0.1
    certificateWeight = 0.2
    return (secureChannelWeight * secureChannelWeightGrade) + (apparmorWeight * apparmorGrade) + (certificateWeight * certificateGrade)

def checkURLConnection(url):
    # https://stackoverflow.com/questions/65955022/python-check-if-webpage-is-http-or-https
    url = urlparse("http://" + hostname + ":" + port)
    conn = http.client.HTTPConnection(url.netloc)
    conn.request("HEAD", url.path)
    if conn.getresponse():
        return True
    else:
        return False

def checkCertificate():
    #if "Certificate" in (subprocess.run(["microk8s.kubectl", "-n", "sock-shop", "get", "secret"])):
    #    if "Expired" in (subprocess.run(["microk8s.kubectl", "-n", "sock-shop", "get", "secret"])):
    #        return
    #    else:
    #        return 5
    #else:
    #    return -5
    #
    ### DNS?
    #

    hostname = "10.161.2.161"
    port = "30001"

    context = ssl.create_default_context()

    # https://github.com/echovue/Operations/blob/master/PythonScripts/TLSValidator.py
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            certificate = ssock.getpeercert()

    certExpires = datetime.datetime.strptime(certificate['notAfter'], '%b %d %H:%M:%S %Y %Z')
    daysToExpiration = (certExpires - datetime.datetime.now()).days

    if checkURLConnection("http://" + hostname + ":" + port):
        if check_url("https://" + hostname + ":" + port):
            if daysToExpiration <  0:
                return 0
            elif daysToExpiration >  0:
                return 5
        else:
            return -5
    else:
        # What should we return here?
        return 0

def prometheusRequest():

    print("Start Loop")

    for x in parameterQueriesToValues:
        prometheusResponse = requests.get(PROMETHEUS + '/container_spec_cpu_quota', params={'query': x})
        prometheusResponseJson = prometheusResponse.json()
        data = prometheusResponseJson["data"]
        result = data["result"][0]  # uptime: [0] carts, [1] shipping, [2] orders, container_spec_cpu_quota: [0] carts-77b9db4898-27w9m
        parameterQueriesToValues[x] = result["value"]
        print("At time", parameterQueriesToValues[x][0], "the result of", x, "was", parameterQueriesToValues[x][1])

    availabilityGrade = availabilityGradeCalculation(parameterQueriesToValues.get('uptime')[1])
    reliabilityGrade = reliabilityGradeCalculation(responseErrorsGrade, logLevelGrade)
    performanceGrade = performanceGradeCalculation(parameterQueriesToValues.get('gauge_response_metrics')[1],
                                                   throughputGrade,
                                                   parameterQueriesToValues.get('container_spec_cpu_quota')[1])
    correctnessGrade = correctnessGradeCalculation(numberOfCorrectCallsGrade)
    securityGrade = securityGradeCalculation(secureChannelWeightGrade, apparmorGrade, certificateGrade)

    parameterGradeList = [availabilityGrade, reliabilityGrade, performanceGrade, correctnessGrade, securityGrade]
    #parameterGradeList = [availabilityGrade, performanceGrade]
    trustCalculation(parameterGradeList)


def main():
    print("Main Call!")
    while True:
        prometheusRequest()
        time.sleep(30)


if __name__ == "__main__":
    main()
