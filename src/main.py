import time
import AvailabilityGradeCalculation
import ReliabilityGradeCalculation
import PerformanceGradeCalculation
import CorrectnessGradeCalculation
import SecurityGradeCalculation
import schedule
import json
from datetime import datetime


PROMETHEUS = 'http://10.161.2.161:31090/'
SOCKSHOP = 'http://10.161.2.161:30001/'
UPDATE_INTERVAL = 5
HISTORIC_DATA = 24
EXTERN_URL = ["moodle.zhaw.ch", "zhaw.ch", "mozilla.org", "google.com", "wikipedia.org"]

trustScore = []
date = []

availabilityGradeList = []
reliabilityGradeList = []
performanceGradeList = []
correctnessGradeList = []
securityGradeList = []

uptimeGradeList = []
responseErrorsGradeList = []
logLevelGradeList = []
patchLevelGradeList = []
responseTimeGradeList = []
memoryUsageGradeList = []
diskReadGradeList = []
diskWriteGradeList = []
cpuUsageGradeList = []
callCorrectnessGradeList = []
appArmorGradeList = []
certificateGradeList = []
vulnerabilityGradeList = []

singleUptimeGradeList = []
singleResponseErrorsGradeList = []
singleLogLevelGradeList = []
singlePatchLevelGradeList = []
singleResponseTimeGradeList = []
singleMemoryUsageGradeList = []
singleDiskReadGradeList = []
singleDiskWriteGradeList = []
singleCpuUsageGradeList = []
singleCallCorrectnessGradeList = []
singleAppArmorGradeList = []
singleCertificateGradeList = []
singleNiktoCheckGradeList = []
singleSsllabsCheckGradeList = []
singleHttpobsCheckGradeList = []

availabilityGradeCalculation = AvailabilityGradeCalculation.AvailabilityGradeCalculation(PROMETHEUS, UPDATE_INTERVAL, HISTORIC_DATA)
reliabilityGradeCalculation = ReliabilityGradeCalculation.ReliabilityGradeCalculation(PROMETHEUS, UPDATE_INTERVAL, HISTORIC_DATA)
performanceGradeCalculation = PerformanceGradeCalculation.PerformanceGradeCalculation(PROMETHEUS, UPDATE_INTERVAL, HISTORIC_DATA)
correctnessGradeCalculation = CorrectnessGradeCalculation.CorrectnessGradeCalculation(SOCKSHOP, UPDATE_INTERVAL, HISTORIC_DATA)
securityGradeCalculation = SecurityGradeCalculation.SecurityGradeCalculation(EXTERN_URL)


def trustCalculation():
    availabilityGrade = availabilityGradeCalculation.calculateGrade()
    availabilityWeight = 0.2
    print("AvailabilityGrade: ", availabilityGrade)

    reliabilityGrade = reliabilityGradeCalculation.calculateGrade()
    reliabilityWeight = 0.2
    print("ReliabilityGrade: ", reliabilityGrade)

    performanceGrade = performanceGradeCalculation.calculateGrade()
    performanceWeight = 0.2
    print("PerformanceGrade: ", performanceGrade)

    correctnessGrade = correctnessGradeCalculation.calculateGrade()
    correctnessWeight = 0.2
    print("CorrectnessGrade: ", correctnessGrade)

    securityGrade = securityGradeCalculation.calculateGrade()
    securityWeight = 0.2
    print("SecurityGrade: ", securityGrade)

    trustScore.append(
        (availabilityWeight * availabilityGrade + reliabilityWeight * reliabilityGrade + performanceWeight *
         performanceGrade + correctnessWeight * correctnessGrade + securityWeight * securityGrade))

    date.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    trustScoreDict = [{
        "Timestamp": date,
        "Trustscore": trustScore
    }]

    with open('trustscore.json', 'w') as fp:
        fp.write(json.dumps(trustScoreDict))

    availabilityGradeList.append(availabilityGrade)
    reliabilityGradeList.append(reliabilityGrade)
    performanceGradeList.append(performanceGrade)
    correctnessGradeList.append(correctnessGrade)
    securityGradeList.append(securityGrade)

    parameterScoreDict = [{
            "Timestamp": date,
            "availabilityGrade": availabilityGradeList,
            "reliabilityGrade": reliabilityGradeList,
            "performanceGrade": performanceGradeList,
            "correctnessGrade": correctnessGradeList,
            "securityGrade": securityGradeList
        }]

    with open('parameterscore.json', 'w') as fp:
        fp.write(json.dumps(parameterScoreDict))

    uptimeGradeList.append(availabilityGradeCalculation.getUptimeGrade())
    responseErrorsGradeList.append(reliabilityGradeCalculation.getResponseErrorGrade())
    logLevelGradeList.append(reliabilityGradeCalculation.getLogLevelGrade())
    patchLevelGradeList.append(reliabilityGradeCalculation.getPatchLevelGrade())
    responseTimeGradeList.append(performanceGradeCalculation.getResponseTimeGrade())
    memoryUsageGradeList.append(performanceGradeCalculation.getMemoryUsageGrade())
    diskReadGradeList.append(performanceGradeCalculation.getDiskReadGrade())
    diskWriteGradeList.append(performanceGradeCalculation.getDiskWriteGrade())
    cpuUsageGradeList.append(performanceGradeCalculation.getCpuUsageGrade())
    callCorrectnessGradeList.append(correctnessGradeCalculation.getCallCorrectnessGrade())
    appArmorGradeList.append(securityGradeCalculation.getAppArmorGrade())
    certificateGradeList.append(securityGradeCalculation.getCertificateGrade())
    vulnerabilityGradeList.append(securityGradeCalculation.getVulnerabilityScanGrade())

    subParameterScoreDict = [{
            "Timestamp": date,
            "uptimeGrade": uptimeGradeList,
            "responseErrorGrade": responseErrorsGradeList,
            "LogLevelGrade": logLevelGradeList,
            "PatchLevelGrade": patchLevelGradeList,
            "ResponseTimeGrade": responseTimeGradeList,
            "MemoryUsageGrade": memoryUsageGradeList,
            "DiskReadGrade": diskReadGradeList,
            "DiskWriteGrade": diskWriteGradeList,
            "cpuUsageGrade": cpuUsageGradeList,
            "callCorrectnessGrade": callCorrectnessGradeList,
            "AppArmorGrade": appArmorGradeList,
            "CertificateGrade": certificateGradeList,
            "VulnerabilityGrade": vulnerabilityGradeList
        }]

    with open('subparameterscore.json', 'w') as fp:
        fp.write(json.dumps(subParameterScoreDict))

    singleUptimeGradeList.append(availabilityGradeCalculation.getSingleUptimeGrade())
    singleResponseErrorsGradeList.append(reliabilityGradeCalculation.getSingleResponseErrorGrade())
    singleLogLevelGradeList.append(reliabilityGradeCalculation.getSingleLogLevelGrade())
    singlePatchLevelGradeList.append(reliabilityGradeCalculation.getPatchLevelGrade())
    singleResponseTimeGradeList.append(performanceGradeCalculation.getSingleResponseTimeGrade())
    singleMemoryUsageGradeList.append(performanceGradeCalculation.getSingleMemoryUsageGrade())
    singleDiskReadGradeList.append(performanceGradeCalculation.getSingleDiskReadGrade())
    singleDiskWriteGradeList.append(performanceGradeCalculation.getSingleDiskWriteGrade())
    singleCpuUsageGradeList.append(performanceGradeCalculation.getSingleCpuUsageGrade())
    singleCallCorrectnessGradeList.append(correctnessGradeCalculation.getSingleCallCorrectnessGrade())
    singleAppArmorGradeList.append(securityGradeCalculation.getAppArmorGrade())
    singleCertificateGradeList.append(securityGradeCalculation.getCertificateGrade())
    singleNiktoCheckGradeList.append(securityGradeCalculation.getNiktoCheckGrade())
    singleSsllabsCheckGradeList.append(securityGradeCalculation.getSsllabsCheckGrade())
    singleHttpobsCheckGradeList.append(securityGradeCalculation.getHttpobsCheckGrade())

    singleSubParameterScoreDict = [{
            "Timestamp": date,
            "uptimeGrade": singleUptimeGradeList,
            "responseErrorGrade": singleResponseErrorsGradeList,
            "LogLevelGrade": singleLogLevelGradeList,
            "PatchLevelGrade": singlePatchLevelGradeList,
            "ResponseTimeGrade": singleResponseTimeGradeList,
            "MemoryUsageGrade": singleMemoryUsageGradeList,
            "DiskReadGrade": singleDiskReadGradeList,
            "DiskWriteGrade": singleDiskWriteGradeList,
            "cpuUsageGrade": singleCpuUsageGradeList,
            "callCorrectnessGrade": singleCallCorrectnessGradeList,
            "AppArmorGrade": singleAppArmorGradeList,
            "CertificateGrade": singleCertificateGradeList,
            "NiktoCheckGrade": singleNiktoCheckGradeList,
            "SsllabsCheckGrade": singleSsllabsCheckGradeList,
            "HttpobsCheckGrade": singleHttpobsCheckGradeList,

        }]

    with open('singlesubparameterscore.json', 'w') as fp:
        fp.write(json.dumps(singleSubParameterScoreDict))


def initialCalculation():
    print("Initial Calculation")
    availabilityGradeCalculation.initialCalculation()
    reliabilityGradeCalculation.initialCalculation()
    performanceGradeCalculation.initialCalculation()
    correctnessGradeCalculation.initialCalculation()
    securityGradeCalculation.initialCalculation()
    trustCalculation()


def update():
    print("Update")
    try:
        availabilityGradeCalculation.update()
    except Exception as e:
        print(e)
    try:
        reliabilityGradeCalculation.update()
    except Exception as e:
        print(e)
    try:
        performanceGradeCalculation.update()
    except Exception as e:
        print(e)
    try:
        correctnessGradeCalculation.update()
    except Exception as e:
        print(e)

    trustCalculation()


def dailyUpdate():
    print("Daily Update")
    try:
        reliabilityGradeCalculation.dailyUpdate()
    except Exception as e:
        print(e)

    try:
        securityGradeCalculation.dailyUpdate()
    except Exception as e:
        print(e)


def main():
    print("Main Call!")
    initialCalculation()
    schedule.every(UPDATE_INTERVAL).minutes.do(update)
    schedule.every(2).minutes.do(dailyUpdate)

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()
