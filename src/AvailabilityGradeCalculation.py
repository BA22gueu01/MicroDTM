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

    def calculateUptime(self, firstValue, secondValue):
        print(float(firstValue[0]))
        print(float(secondValue[0]))
        print(float(firstValue[1]))
        print(float(secondValue[1]))

        return (float(firstValue[0]) - float(secondValue[0]) * 1000) / ((float(firstValue[1]) - float(secondValue[1])))

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
            grade = grade + self.calculateUptime(value[0], value[1])
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
                grade = grade + self.calculateUptime(value[i], value[i + 1])
                counter = counter + 1
            grade = grade / counter
            print("uptime Grade: ", grade)
            self.addNewGrade(grade)
