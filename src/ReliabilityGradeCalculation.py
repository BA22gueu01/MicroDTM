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
        print("ResponseErrorGrade")
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
        print("uptime Grade: ", newGrade)
        length = len(grades) - 1
        for x in range(length):
            grades[x] = grades[x + 1]
        grades[length] = newGrade

    def dailyUpdate(self):
        self.calculatePatchLevelGrade()

    def update(self):
        status200Values = self.prometheusRequest.makeRequest('counter_status_200_carts_customerId_items')
        status500Values = self.prometheusRequest.makeRequest('counter_status_500_carts_customerId_items')
        self.calculateResponseErrorGrade(int(status200Values[1]) - int(status200Values[0]), int(status500Values[1]) - int(status500Values[0]))
        self.calculateLogLevelGrade()

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
        status200Values = self.prometheusRequest.makeRequest('counter_status_200_carts_customerId_items_history')
        status500Values = self.prometheusRequest.makeRequest('counter_status_500_carts_customerId_items_history')
        length = len(status200Values) - 1
        for x in range(length):
            self.calculateResponseErrorGrade(int(status200Values[x + 1]) - int(status200Values[x]), int(status500Values[x + 1]) - int(status500Values[x]))
        print(self.responseErrorsGrades)

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
