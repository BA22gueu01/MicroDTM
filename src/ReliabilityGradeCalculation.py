import LogLevelCheck
import PatchLevelCheck
import PrometheusRequest




class ReliabilityGradeCalculation:

    def __init__(self, prometheus):
        self.logLevelCheck = LogLevelCheck.LogLevelCheck()
        self.patchLevelCheck = PatchLevelCheck.PatchLevelCheck()
        self.prometheusRequest = PrometheusRequest.PrometheusRequest(prometheus)

    def calculate(self):
        responseErrorsWeight = 0.4
        logLevelWeight = 0.3
        patchLevelWeight = 0.3

        logLevelGrade = self.logLevelCheck.getLoglevelGrade()
        patchLevelGrade = self.patchLevelCheck.getPatchLevelGrade()

        responseErrorsGrade200 = self.prometheusRequest.makeRequest('counter_status_200_carts_customerId_items')[1]
        responseErrorsGrade500 = self.prometheusRequest.makeRequest('counter_status_500_carts_customerId_items')[1]

        responseErrorsGrade = int(responseErrorsGrade500) / int(responseErrorsGrade200)

        if 0 == responseErrorsGrade < 0.25:
            responseErrorsGrade = 5
        elif 0.25 == responseErrorsGrade < 0.5:
            responseErrorsGrade = 0
        else:
            responseErrorsGrade = -5

        return (responseErrorsWeight * responseErrorsGrade) + (logLevelWeight * logLevelGrade) + (
                    patchLevelWeight * patchLevelGrade)
