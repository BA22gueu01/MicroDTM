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

        return grade

    def addNewGrade(self, newGrade, grades):
        length = len(grades) - 1
        for x in range(length):
            grades[x] = grades[x + 1]
        grades[length] = newGrade

    def dailyUpdate(self):
        self.calculatePatchLevelGrade()

    def update(self):
        status200Values = self.prometheusRequest.makeRequest('counter_status_200_carts_customerId_items')
        status500Values = self.prometheusRequest.makeRequest('counter_status_500_carts_customerId_items')
        self.subGradeCalculation(status200Values, status500Values)

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
        self.subGradeCalculation(status200Values, status500Values)

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

    def subGradeCalculation(self, values200, values500, ):

        if values200 == [0, 0] or values500 == [0, 0]:
            grade = -5
            self.addNewGrade(grade, self.responseErrorsGrades)
            print("Response Error grade: ", grade)

        else:
            length = 0
            for value in values200:
                if len(value) > length:
                    length = len(value)

            for x in range(length - 1):
                grade = 0
                counter = 0
                for y in range(min(len(values200), len(values500))):
                    if x < len(values200[y]) - 1:
                        diff = len(values200[y]) - len(values500[y])
                        if x - diff < -1:
                            value500 = 0
                        elif x - diff == -1:
                            value500 = int(values500[y][0][1])
                        else:
                            value500 = int(values500[y][x + 1 - diff][1]) - int(values500[y][x - diff][1])
                        # noinspection PyTypeChecker
                        grade = grade + self.calculateResponseErrorGrade(
                            int(values200[y][x + 1][1]) - int(values200[y][x][1]), value500)
                        counter = counter + 1
                grade = grade / counter
                self.addNewGrade(grade, self.responseErrorsGrades)
                print("Response Error grade: ", grade)
