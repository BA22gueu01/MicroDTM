import LogLevelCheck
import PatchLevelCheck
import PrometheusRequest
import numpy


class ReliabilityGradeCalculation:

    def __init__(self, prometheus):
        self.logLevelCheck = LogLevelCheck.LogLevelCheck()
        self.patchLevelCheck = PatchLevelCheck.PatchLevelCheck()
        self.prometheusRequest = PrometheusRequest.PrometheusRequest(prometheus)
        self.responseErrorsGrades = numpy.zeros(24)
        self.responseErrorsWeight = 0.4
        self.logLevelGrades = numpy.zeros(24)
        self.logLevelWeight = 0.2
        self.patchLevelGrade = 0
        self.patchLevelWeight = 0.4
        self.lastLogErrorCount = 0

    def calculateGrade(self):

        return (self.responseErrorsWeight * numpy.average(self.responseErrorsGrades)) \
                    + (self.logLevelWeight * numpy.average(self.logLevelGrades)) \
                    + (self.patchLevelWeight * self.patchLevelGrade)

    def calculatePatchLevelGrade(self):
        self.patchLevelGrade = self.patchLevelCheck.getPatchLevelGrade()
        print("PatchLevelGrade: ", self.patchLevelGrade)

    def calculateResponseErrorGrade(self, status200Value, status500Value):
        if status200Value == 0:
            status200Value = 1

        responseErrorsGrade = status500Value / status200Value

        if 0 <= responseErrorsGrade < 0.25:
            grade = 5
        elif 0.25 <= responseErrorsGrade < 0.5:
            grade = 0
        else:
            grade = -5

        print("ResponseErrorGrade: ", grade)
        self.addNewGrade(grade, self.responseErrorsGrades)

    def addNewGrade(self, newGrade, grades):
        length = len(grades) - 1
        for x in range(length):
            grades[x] = grades[x + 1]
        grades[length] = newGrade

    def dailyUpdate(self):
        self.calculatePatchLevelGrade()

    def update(self):
        status200Values = self.prometheusRequest.makeRequest('counter_status_200_carts_customerId_items')[0]
        status500Values = self.prometheusRequest.makeRequest('counter_status_500_carts_customerId_items')[0]
        self.calculateResponseErrorGrade(int(status200Values[1][1]) - int(status200Values[0][1]),
                                         int(status500Values[1][1]) - int(status500Values[0][1]))

        logLevelErrorCount = self.logLevelCheck.getLogLevelCount()
        newLogLevelErrorCount = logLevelErrorCount - self.lastLogErrorCount
        self.lastLogErrorCount = logLevelErrorCount

        if newLogLevelErrorCount > 40:
            grade = -5
        elif 40 == logLevelErrorCount > 10:
            grade = 0
        else:
            grade = 5
        self.addNewGrade(grade, self.logLevelGrades)
        print("LogLevelGrade: ", grade)

    def initialCalculation(self):
        status200Values = self.prometheusRequest.makeRequest('counter_status_200_carts_customerId_items_history')[0]
        status500Values = self.prometheusRequest.makeRequest('counter_status_500_carts_customerId_items_history')[0]
        length = min(len(status200Values), len(status500Values)) - 1
        for x in range(length):
            self.calculateResponseErrorGrade(int(status200Values[x + 1][1]) - int(status200Values[x][1]),
                                             int(status500Values[x + 1][1]) - int(status500Values[x][1]))

        logLevelErrorCount = self.logLevelCheck.getLogLevelCount()
        if logLevelErrorCount > 3000:
            grade = -5
        elif 3000 == logLevelErrorCount > 1000:
            grade = 0
        else:
            grade = 5
        self.addNewGrade(grade, self.logLevelGrades)
        self.lastLogErrorCount = logLevelErrorCount
        print("LogLevelGrade: ", grade)

        self.calculatePatchLevelGrade()

    def subGradeCalculation(self, values200, values500,):
        if values == [0, 0]:
            grade = -5
            self.addNewGrade(grade, gradeArray)
            print(gradeName, grade)

        else:
            length = 0
            for value in values:
                if len(value) > length:
                    length = len(value)

            for x in range(length):
                grade = 0
                counter = 0
                for y in range(len(values)):
                    if x < len(values[y]):
                        grade = grade + func(values[y][x])
                        counter = counter + 1
                grade = grade / counter
                self.addNewGrade(grade, gradeArray)
                print(gradeName, grade)
