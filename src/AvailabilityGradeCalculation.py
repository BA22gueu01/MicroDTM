import PrometheusRequest
import numpy


class AvailabilityGradeCalculation:

    def __init__(self, prometheus):
        self.prometheusRequest = PrometheusRequest.PrometheusRequest(prometheus)
        self.uptimeGrade = 0
        self.uptimeWeight = 1
        self.uptimeGrades = numpy.zeros(24)

    def calculateGrade(self):
        print(self.uptimeGrades)
        print(numpy.average(self.uptimeGrades))
        return self.uptimeWeight * numpy.average(self.uptimeGrades)

    def calculateUptimeGrade(self, firstValue, secondValue):
        uptime = ((float(firstValue[1]) - float(secondValue[1])) / ((float(firstValue[0]) - float(secondValue[0])) * 1000)) * 100
        if uptime >= 99.9:
            grade = 5
        elif uptime >= 95:
            grade = 4
        elif uptime >= 90:
            grade = 3
        elif uptime >= 75:
            grade = 0 + ((uptime - 75) / (90 - 75)) * 3
        elif uptime <= 50:
            grade = -5
        else:
            grade = -5 + ((uptime - 50) / (75 - 50)) * 5

        return grade

    def addNewGrade(self, newGrade):
        length = len(self.uptimeGrades) - 1
        for x in range(length):
            self.uptimeGrades[x] = self.uptimeGrades[x + 1]
        self.uptimeGrades[length] = newGrade

    def update(self):
        uptimeValues = self.prometheusRequest.makeRequest("uptime")
        grade = 0
        counter = 0
        print(uptimeValues)
        for value in uptimeValues:
            print(value)
            grade = grade + self.calculateUptimeGrade(value[0], value[1])
            counter = counter + 1
        grade = grade/counter
        print("uptime Grade: ", grade)
        self.addNewGrade(grade)

    def initialCalculation(self):
        uptimeValues = self.prometheusRequest.makeRequest("uptime_history")
        length = len(uptimeValues[0]) - 1
        for x in range(length):
            grade = 0
            counter = 0
            i = length - x
            for value in uptimeValues:
                grade = grade + self.calculateUptimeGrade(value[i - 1], value[i])
                counter = counter + 1
            grade = grade / counter
            print("uptime Grade: ", grade)
            self.addNewGrade(grade)
