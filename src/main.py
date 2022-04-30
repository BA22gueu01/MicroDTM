import requests
import time
import CertificateCheck
import ReliabilityGradeCalculation
import ApparmorCheck
import CheckCVE
import GetPods

PROMETHEUS = 'http://10.161.2.161:31090/'
PARAMETERWEIGHT = 0.2

KEYS = ["uptime", "counter_status_200_carts_customerId_items", "counter_status_500_carts_customerId_items",
        "gauge_response_metrics", "container_spec_cpu_quota", "disk_read", "disk_write"]
parameterQueriesToValues = {k: None for k in KEYS}

reliabilityGradeCalculation = ReliabilityGradeCalculation.ReliabilityGradeCalculation(PROMETHEUS)


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
    for x in range(len(uptimeValues) - 1):
        # uptimeGrade = (uptimeGrade - pastUptimeGrade) / ((actualTime - pastTime)*1000)
        uptimeGrade.append((int(uptimeValues[counter][1]) - int(uptimeValues[counter - 1][1])) / (
                (uptimeValues[counter][0] - uptimeValues[counter - 1][0]) * 1000))
        counter += 1

    # return uptimeWeight multiplicated with the average value of the uptimeGrade list
    return uptimeWeight * (sum(uptimeGrade) / len(uptimeGrade))


def performanceGradeCalculation(responseTimeGrade, cpuUsageGrade, diskReadGrade, diskWriteGrade):
    responseTimeWeight = 0.4
    throughputWeight = 0.2
    cpuUsageWeight = 0.2
    diskWeight = 0.1

    responseTimeGrade = int(responseTimeGrade)

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

    diskReadGrade = float(diskReadGrade)
    diskWriteGrade = float(diskWriteGrade)

    if diskReadGrade or diskWriteGrade > 0.04:
        diskReadGrade, diskWriteGrade = -5
    elif diskReadGrade or diskWriteGrade > 0.025:
        diskReadGrade, diskWriteGrade = 0
    else:
        diskReadGrade, diskWriteGrade = 5

    return (responseTimeWeight * responseTimeGrade) + (cpuUsageWeight * cpuUsageGrade) + (
                diskWeight * diskReadGrade) + (diskWeight * diskWriteGrade)


def correctnessGradeCalculation(numberOfCorrectCallsGrade):
    numberOfCorrectCallsWeight = 1.0

    return numberOfCorrectCallsWeight * numberOfCorrectCallsGrade


def securityGradeCalculation(apparmorGrade, certificateGrade):
    apparmorWeight = 0.1
    certificateWeight = 0.2
    checkCVE = CheckCVE.CheckCVE()
    checkCVE.checkCVE()

    return (apparmorWeight * apparmorGrade) + (certificateWeight * certificateGrade)


def prometheusRequest():
    print("Start Loop")
    getPods = GetPods.GetPods()
    pods = getPods.getPods()
    print(pods)
    print(pods[0])
    getPods.getContainers(pods[0])

    instance = "10.161.2.161:9100"
    job = "node-exporter"

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
        # https://brian-candler.medium.com/interpreting-prometheus-metrics-for-linux-disk-i-o-utilization-4db53dfedcfc
        elif x == "disk_read":
            diskReadCalculation = 'rate(node_disk_read_time_seconds_total{instance="' + instance + '",job="' + job + '"}[5m]) / rate(node_disk_reads_completed_total{instance="' + instance + '",job="' + job + '"}[5m])'
            prometheusResponse = requests.get(PROMETHEUS + '/api/v1/query', params={'query': diskReadCalculation})
        elif x == "disk_write":
            diskWriteCalculation = 'rate(node_disk_write_time_seconds_total{instance="' + instance + '",job="' + job + '"}[5m]) / rate(node_disk_writes_completed_total{instance="' + instance + '",job="' + job + '"}[5m])'
            prometheusResponse = requests.get(PROMETHEUS + '/api/v1/query', params={'query': diskWriteCalculation})
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

    # print(parameterQueriesToValues)
    availabilityGrade = availabilityGradeCalculation(parameterQueriesToValues.get('uptime'))

    reliabilityGrade = reliabilityGradeCalculation.calculate()

    performanceGrade = performanceGradeCalculation(parameterQueriesToValues.get('gauge_response_metrics')[1],
                                                   # throughputGrade,
                                                   parameterQueriesToValues.get('container_spec_cpu_quota')[1],
                                                   parameterQueriesToValues.get('disk_read')[1],
                                                   parameterQueriesToValues.get('disk_write')[1])
    # performanceGrade = performanceGradeCalculation(parameterQueriesToValues.get('gauge_response_metrics'),
    # throughputGrade,
    #                                               parameterQueriesToValues.get('container_spec_cpu_quota'))

    # correctnessGrade = correctnessGradeCalculation(numberOfCorrectCallsGrade)

    certificateCheck = CertificateCheck.CertificateCheck("zhaw.ch", "443")
    apparmorCheck = ApparmorCheck.ApparmorCheck()
    securityGrade = securityGradeCalculation(apparmorCheck.checkApparmor(),
                                             certificateCheck.checkCertificate())

    # parameterGradeList = [availabilityGrade, reliabilityGrade, performanceGrade, correctnessGrade, securityGrade]
    parameterGradeList = [availabilityGrade, reliabilityGrade, performanceGrade, securityGrade]
    trustCalculation(parameterGradeList)


def main():
    print("Main Call!")
    while True:
        prometheusRequest()
        time.sleep(30)


if __name__ == "__main__":
    main()
