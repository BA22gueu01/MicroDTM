import time
import AvailabilityGradeCalculation
import ReliabilityGradeCalculation
import PerformanceGradeCalculation
import CorrectnessGradeCalculation
import SecurityGradeCalculation
import schedule
import csv
from datetime import datetime


PROMETHEUS = 'http://10.161.2.161:31090/'
SOCKSHOP = 'http://10.161.2.161:30001/'

trustScore = []
date = []

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

    date.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    trustScoreDict = [{
        "Timestamp": date,
        "Trustscore": trustScore
    }]

    field_names = ["Timestamp", "Trustscore"]

    with open('trustscore.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=",")
        writer.writeheader()
        writer.writerows(trustScoreDict)

    #print("Trustscore: ", trustScore)
    with open('trustscore.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            print(", ".join(row))


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
