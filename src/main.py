import time
import AvailabilityGradeCalculation
import ReliabilityGradeCalculation
import PerformanceGradeCalculation
import CorrectnessGradeCalculation
import SecurityGradeCalculation
import schedule

PROMETHEUS = 'http://10.161.2.161:31090/'
SOCKSHOP = 'http://10.161.2.161:30001/'

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

    trustScore = (availabilityWeight * availabilityGrade + reliabilityWeight * reliabilityGrade + performanceWeight *
                  performanceGrade + correctnessWeight * correctnessGrade + securityWeight * securityGrade)

    print("Trustscore: ", trustScore)


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
    availabilityGradeCalculation.update()
    reliabilityGradeCalculation.update()
    performanceGradeCalculation.update()
    correctnessGradeCalculation.update()
    trustCalculation()


def dailyUpdate():
    print("Daily Update")
    reliabilityGradeCalculation.dailyUpdate()
    securityGradeCalculation.dailyUpdate()


def main():
    print("Main Call!")
    initialCalculation()
    schedule.every().hour.do(update)
    schedule.every().day.do(dailyUpdate)

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()

