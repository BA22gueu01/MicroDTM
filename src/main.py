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
UPDATE_INTERVAL = 60
HISTORIC_DATA = 24

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

availabilityGradeCalculation = AvailabilityGradeCalculation.AvailabilityGradeCalculation(PROMETHEUS)
reliabilityGradeCalculation = ReliabilityGradeCalculation.ReliabilityGradeCalculation(PROMETHEUS)
performanceGradeCalculation = PerformanceGradeCalculation.PerformanceGradeCalculation(PROMETHEUS)
correctnessGradeCalculation = CorrectnessGradeCalculation.CorrectnessGradeCalculation(SOCKSHOP)
securityGradeCalculation = SecurityGradeCalculation.SecurityGradeCalculation()


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
            "CertificateGrade": certificateGradeList
        }]

    with open('subparameterscore.json', 'w') as fp:
        fp.write(json.dumps(subParameterScoreDict))


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
    schedule.every(HISTORIC_DATA * UPDATE_INTERVAL).minutes.do(dailyUpdate)

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()
