import PrometheusRequest
import numpy



class AvailabilityGradeCalculation:

    def __init__(self, prometheus, updateInterval, historicData):
        self.prometheusRequest = PrometheusRequest.PrometheusRequest(prometheus, updateInterval, historicData)
        self.uptimeWeight = 1
        self.uptimeGrades = numpy.zeros(historicData)

    def calculateGrade(self):
        return self.uptimeWeight * numpy.average(self.uptimeGrades)

    def getUptimeGrade(self):
        return numpy.average(self.uptimeGrades)

    def getSingleUptimeGrade(self):
        return self.uptimeGrades[len(self.uptimeGrades) - 1]

    def calculateUptimeGrade(self, firstValue, secondValue):
        uptime = ((float(firstValue[1]) - float(secondValue[1])) /
                  ((float(firstValue[0]) - float(secondValue[0])) * 1000)) * 100
        if uptime >= 99.9:
            grade = 5
        elif uptime >= 95:
            grade = 4 + ((uptime - 95) / (99.9 - 95))
        elif uptime >= 90:
            grade = 3 + ((uptime - 90) / (95 - 90))
        elif uptime >= 75:
            grade = 0 + ((uptime - 75) / (90 - 75)) * 3
        elif uptime <= 50:
            grade = -5
        else:
            grade = -5 + ((uptime - 50) / (75 - 50)) * 5

        return grade

    def addNewGrade(self, newGrade):
        print("uptime Grade: ", newGrade)
        length = len(self.uptimeGrades) - 1
        for x in range(length):
            self.uptimeGrades[x] = self.uptimeGrades[x + 1]
        self.uptimeGrades[length] = newGrade

    def update(self):
        uptimeValues = self.prometheusRequest.makeRequest("uptime")
        self.subGradeCalculation(uptimeValues)

    def initialCalculation(self):
        uptimeValues = self.prometheusRequest.makeRequest("uptime_history")
        self.subGradeCalculation(uptimeValues)

    def subGradeCalculation(self, values):
        if values == [0, 0]:
            grade = 0
            self.addNewGrade(grade)

        else:
            length = 0
            for value in values:
                if len(value) > length:
                    length = len(value)

            for x in range(length - 1):
                grade = 0
                counter = 0
                for y in range(len(values)):
                    if x < len(values[y]) - 1:
                        grade = grade + self.calculateUptimeGrade(values[y][x + 1], values[y][x])
                        counter = counter + 1
                grade = grade / counter
                self.addNewGrade(grade)
