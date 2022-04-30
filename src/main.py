import time
import AvailabilityGradeCalculation
import ReliabilityGradeCalculation
import PerformanceGradeCalculation
import SecurityGradeCalculation
import schedule

PROMETHEUS = 'http://10.161.2.161:31090/'

availabilityGradeCalculation = AvailabilityGradeCalculation.AvailabilityGradeCalculation(PROMETHEUS)
reliabilityGradeCalculation = ReliabilityGradeCalculation.ReliabilityGradeCalculation(PROMETHEUS)
performanceGradeCalculation = PerformanceGradeCalculation.PerformanceGradeCalculation(PROMETHEUS)
securityGradeCalculation = SecurityGradeCalculation.SecurityGradeCalculation()


def trustCalculation():
    availabilityGrade = availabilityGradeCalculation.calculateGrade()
    availabilityWeight = 0.2

    reliabilityGrade = reliabilityGradeCalculation.calculateGrade()
    reliabilityWeight = 0.2

    performanceGrade = 0
    performanceWeight = 0.2

    correctnessGrade = 0
    correctnessWeight = 0.2

    securityGrade = 0
    securityWeight = 0.2

    trustScore = (availabilityWeight * availabilityGrade + reliabilityWeight * reliabilityGrade + performanceWeight *
                  performanceGrade + correctnessWeight * correctnessGrade + securityWeight * securityGrade)

    print("Trustscore: ", trustScore)


def correctnessGradeCalculation(numberOfCorrectCallsGrade):
    numberOfCorrectCallsWeight = 1.0

    return numberOfCorrectCallsWeight * numberOfCorrectCallsGrade


def initialCalculation():
    availabilityGradeCalculation.initialCalculation()
    reliabilityGradeCalculation.initialCalculation()
    performanceGradeCalculation.initialCalculation()
    securityGradeCalculation.initialCalculation()
    trustCalculation()


def update():
    availabilityGradeCalculation.update()
    reliabilityGradeCalculation.update()
    performanceGradeCalculation.update()
    trustCalculation()


def hourlyUpdate():
    trustCalculation()


def dailyUpdate():
    reliabilityGradeCalculation.dailyUpdate()
    securityGradeCalculation.dailyUpdate()
    trustCalculation()


def main():
    print("Main Call!")
    initialCalculation()
    schedule.every(30).seconds.do(update)
    schedule.every().hour.do(hourlyUpdate)
    schedule.every().day.do(dailyUpdate)

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()

