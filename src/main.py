import requests
import time
import CertificateCheck
import LogLevelCheck
import ApparmorCheck
import CheckCVE
import CheckPatchLevel
import GetPods

PROMETHEUS = 'http://10.161.2.161:31090/'
PARAMETERWEIGHT = 0.2

KEYS = ["uptime", "counter_status_200_carts_customerId_items", "counter_status_500_carts_customerId_items",
        "gauge_response_metrics", "container_spec_cpu_quota"]
parameterQueriesToValues = {k: None for k in KEYS}

"""
parameterQueriesToValues = {"uptime" : [[20, 10],[10, 50]], "counter_status_200_carts_customerId_items" : 39999,
                            "counter_status_500_carts_customerId_items" :  6, "gauge_response_metrics" : 5,
                            "container_spec_cpu_quota" : 0.88}
"""

def trustCalculation(parameterGradeList):
    trustScore = 0

    for x in range(len(parameterGradeList)):
        trustScore = trustScore + (parameterGradeList[x] * PARAMETERWEIGHT)

    print("Trustscore: ", trustScore)


def availabilityGradeCalculation(uptimeValues):
    uptimeWeight = 1
    counter = 1
    uptimeGrade = []

    # time = seconds, uptime values = milliseconds
    # denominator to milliseconds so that actualTime and uptimeGrade have the same unit of time
    for x in range(len(uptimeValues)-1):
        # uptimeGrade = (uptimeGrade - pastUptimeGrade) / ((actualTime - pastTime)*1000)
        uptimeGrade.append((int(uptimeValues[counter][1]) - int(uptimeValues[counter - 1][1])) / (
                    (uptimeValues[counter][0] - uptimeValues[counter - 1][0]) * 1000))
        counter += 1

    # return uptimeWeight multiplicated with the average value of the uptimeGrade list
    return uptimeWeight * (sum(uptimeGrade) / len(uptimeGrade))


def reliabilityGradeCalculation(responseErrorsGrade200, responseErrorsGrade500, logLevelGrade, patchLevelGrade):
    responseErrorsWeight = 0.4
    logLevelWeight = 0.3
    patchLevelWeight = 0.3

    responseErrorsGrade = int(responseErrorsGrade500) / int(responseErrorsGrade200)
    if 0 == responseErrorsGrade < 0.25:
        responseErrorsGrade = 5
    elif 0.25 == responseErrorsGrade < 0.5:
        responseErrorsGrade = 0
    else:
        responseErrorsGrade = -5

    return (responseErrorsWeight * responseErrorsGrade) + (logLevelWeight * logLevelGrade) + (patchLevelWeight * patchLevelGrade)


#def performanceGradeCalculation(responseTimeGrade, throughputGrade, cpuUsageGrade):
def performanceGradeCalculation(responseTimeGrade, cpuUsageGrade):
    responseTimeWeight = 0.5
    throughputWeight = 0.3
    cpuUsageWeight = 0.2

    responseTimeGrade = int(responseTimeGrade)
    # to be updated
    if responseTimeGrade > 5:
        responseTimeGrade = -5
    elif responseTimeGrade > 2.5:
        responseTimeGrade = 0
    else:
        responseTimeGrade = 5

    # https://github.com/google/cadvisor/issues/2026
    # Get result as percentage
    cpuUsageGrade = float(cpuUsageGrade) * 100
    # to be updated
    if cpuUsageGrade > 0.8:
        cpuUsageGrade = -5
    elif cpuUsageGrade > 0.5:
        cpuUsageGrade = 0
    else:
        cpuUsageGrade = 5

    return (responseTimeWeight * responseTimeGrade) + (cpuUsageWeight * cpuUsageGrade)
    #return (responseTimeWeight * responseTimeGrade) + (throughputWeight * throughputGrade) + (
    #        cpuUsageWeight * cpuUsageGrade)


def correctnessGradeCalculation(numberOfCorrectCallsGrade):
    numberOfCorrectCallsWeight = 1.0

    return numberOfCorrectCallsWeight * numberOfCorrectCallsGrade

def securityGradeCalculation(apparmorGrade, certificateGrade):
#def securityGradeCalculation(secureChannelWeightGrade, apparmorGrade, certificateGrade):

    secureChannelWeight = 0.7
    apparmorWeight = 0.1
    certificateWeight = 0.2
    checkCVE = CheckCVE.CheckCVE()
    checkCVE.checkCVE()

    return (apparmorWeight * apparmorGrade) + (certificateWeight * certificateGrade)
#    return (secureChannelWeight * secureChannelWeightGrade) + (apparmorWeight * apparmorGrade) + (
#                certificateWeight * certificateGrade)


def prometheusRequest():
    print("Start Loop")
    getPods = GetPods.GetPods()
    pods = getPods.getPods()
    getPods.getContainers(pods[0])

    for x in parameterQueriesToValues:
        if x == "uptime":
            prometheusResponse = requests.get(PROMETHEUS + '/api/v1/query?query=uptime[30s:1s]')
        elif x == "container_spec_cpu_quota":
            cpuUsageCalculation = 'sum(rate(container_cpu_usage_seconds_total{name!~".*prometheus.*", image!="", ' \
                                  'container_name!="POD"}[5m])) by (pod_name, container_name)/' \
                                  'sum(container_spec_cpu_quota{name!~".*prometheus.*", image!="", ' \
                                  'container_name!="POD"}/container_spec_cpu_period{name!~".*prometheus.*", ' \
                                  'image!="", container_name!="POD"}) by (pod_name, container_name)'
            prometheusResponse = requests.get(PROMETHEUS + '/api/v1/query', params={'query': cpuUsageCalculation})
        else:
            prometheusResponse = requests.get(PROMETHEUS + '/api/v1/query', params={'query': x})
        prometheusResponseJson = prometheusResponse.json()
        data = prometheusResponseJson["data"]

        # Check if Prometheus result is empty
        if len(data["result"]) == 0:
            result = [0, 0]
            parameterQueriesToValues[x] = result
        else:
            result = data["result"][0]
            if x == "uptime":
                parameterQueriesToValues[x] = result["values"]
            else:
                parameterQueriesToValues[x] = result["value"]

        # uptime: [0] carts, [1] shipping, [2] orders, container_spec_cpu_quota: [0] carts-77b9db4898-27w9m
        # print("At time", parameterQueriesToValues[x][0], "the result of", x, "was", parameterQueriesToValues[x][1])

    print(parameterQueriesToValues)
    availabilityGrade = availabilityGradeCalculation(parameterQueriesToValues.get('uptime'))

    patchLevelCheck = CheckPatchLevel.CheckPatchLevel()
    logLevelCheck = LogLevelCheck.LogLevelCheck()
    reliabilityGrade = reliabilityGradeCalculation(parameterQueriesToValues.get('counter_status_200_carts_customerId_items')[1],
                                                   parameterQueriesToValues.get('counter_status_500_carts_customerId_items')[1],
    #reliabilityGrade = reliabilityGradeCalculation(parameterQueriesToValues.get('counter_status_200_carts_customerId_items'),
    #                                               parameterQueriesToValues.get('counter_status_500_carts_customerId_items'),
                                                   logLevelCheck.checkLoglevel(),
                                                   patchLevelCheck.checkPatchLevel())

    performanceGrade = performanceGradeCalculation(parameterQueriesToValues.get('gauge_response_metrics')[1],
                                                   #throughputGrade,
                                                   parameterQueriesToValues.get('container_spec_cpu_quota')[1])
    #performanceGrade = performanceGradeCalculation(parameterQueriesToValues.get('gauge_response_metrics'),
                                                   #throughputGrade,
    #                                               parameterQueriesToValues.get('container_spec_cpu_quota'))

    #correctnessGrade = correctnessGradeCalculation(numberOfCorrectCallsGrade)

    #certificateCheck = CertificateCheck("10.161.2.161", "30001")
    certificateCheck = CertificateCheck.CertificateCheck("zhaw.ch", "443")
    apparmorCheck = ApparmorCheck.ApparmorCheck()
    #securityGrade = securityGradeCalculation(secureChannelWeightGrade, apparmorCheck.checkApparmor(),
    securityGrade = securityGradeCalculation(apparmorCheck.checkApparmor(),
                                             certificateCheck.checkCertificate())

    #parameterGradeList = [availabilityGrade, reliabilityGrade, performanceGrade, correctnessGrade, securityGrade]
    parameterGradeList = [availabilityGrade, reliabilityGrade, performanceGrade, securityGrade]
    trustCalculation(parameterGradeList)


def main():
    print("Main Call!")
    while True:
        prometheusRequest()
        time.sleep(30)


if __name__ == "__main__":
    main()
