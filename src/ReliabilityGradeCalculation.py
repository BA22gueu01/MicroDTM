import LogLevelCheck
import PatchLevelCheck
import PrometheusRequest


class ReliabilityGradeCalculation:

    def __init__(self, prometheus):
        self.logLevelCheck = LogLevelCheck.LogLevelCheck()
        self.patchLevelCheck = PatchLevelCheck.PatchLevelCheck()
        self.prometheusRequest = PrometheusRequest.PrometheusRequest(prometheus)
        self.logLevelGrade = 0
        self.logLevelWeight = 0.2
        self.patchLevelGrade = 0
        self.patchLevelWeight = 0.4
        self.responseErrorsGrade = 0
        self.responseErrorsWeight = 0.4

    def calculateGrade(self):

        return (self.responseErrorsWeight * self.responseErrorsGrade) + (self.logLevelWeight * self.logLevelGrade) \
                    + (self.patchLevelWeight * self.patchLevelGrade)

    def calculateLogLevelGrade(self):
        self.logLevelGrade = self.logLevelCheck.getLogLevelGrade()

    def calculatePatchLevelGrade(self):
        self.patchLevelGrade = self.patchLevelCheck.getPatchLevelGrade()

    def calculateResponseErrorGrad(self):

        responseErrorsGrade200 = self.prometheusRequest.makeRequest('counter_status_200_carts_customerId_items')[1]
        responseErrorsGrade500 = self.prometheusRequest.makeRequest('counter_status_500_carts_customerId_items')[1]

        responseErrorsGrade = int(responseErrorsGrade500) / int(responseErrorsGrade200)

        if 0 == responseErrorsGrade < 0.25:
            self.responseErrorsGrade = 5
        elif 0.25 == responseErrorsGrade < 0.5:
            self.responseErrorsGrade = 0
        else:
            self.responseErrorsGrade = -5

    def dailyUpdate(self):
        self.calculatePatchLevelGrade()

    def update(self):
        self.calculateLogLevelGrade()
        self.calculateResponseErrorGrad()

    def initialCalculation(self):
        self.calculateLogLevelGrade()
        self.calculateResponseErrorGrad()
        self.calculatePatchLevelGrade()
