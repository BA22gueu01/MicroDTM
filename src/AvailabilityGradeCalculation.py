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

        return (firstValue[0] - secondValue[0]) / ((firstValue[1] - secondValue[1]) * 1000)



        counter = 1
        uptimeGrade = []

        # time = seconds, uptime values = milliseconds
        # denominator to milliseconds so that actualTime and uptimeGrade have the same unit of time
        for x in range(len(uptimeValues) - 1):
            # uptimeGrade = (uptimeGrade - pastUptimeGrade) / ((actualTime - pastTime)*1000)
            uptimeGrade.append((int(uptimeValues[counter][1]) - int(uptimeValues[counter - 1][1])) / (
                    (uptimeValues[counter][0] - uptimeValues[counter - 1][0]) * 1000))
            counter += 1

        self.uptimeGrade = sum(uptimeGrade) / len(uptimeGrade)
        print("uptime Grade: ", self.uptimeGrade)

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
                grade = grade + self.calculateUptime(value[x], value[x + 1])
                counter = counter + 1
            grade = grade / counter
            print("uptime Grade: ", grade)
            self.addNewGrade(grade)


        self.calculateUptimeGrade()
