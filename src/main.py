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

    correctnessGrade = correctnessGradeCalculation.callCorrectnessGrade
    correctnessWeight = 0.2
    print("CorrectnessGrade: ", correctnessGrade)

    securityGrade = securityGradeCalculation.calculateGrade()
    securityWeight = 0.2
    print("SecurityGrade: ", securityGrade)

    trustScore = (availabilityWeight * availabilityGrade + reliabilityWeight * reliabilityGrade + performanceWeight *
                  performanceGrade + correctnessWeight * correctnessGrade + securityWeight * securityGrade)

    print("Trustscore: ", trustScore)


def initialCalculation():
    #availabilityGradeCalculation.initialCalculation()
    #reliabilityGradeCalculation.initialCalculation()
    #performanceGradeCalculation.initialCalculation()
    correctnessGradeCalculation.initialCalculation()
    #securityGradeCalculation.initialCalculation()
    trustCalculation()


def update():
    availabilityGradeCalculation.update()
    reliabilityGradeCalculation.update()
    performanceGradeCalculation.update()
    trustCalculation()


def hourlyUpdate():
    correctnessGradeCalculation.hourlyUpdate()


def dailyUpdate():
    reliabilityGradeCalculation.dailyUpdate()
    securityGradeCalculation.dailyUpdate()


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

