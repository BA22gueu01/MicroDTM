import PrometheusRequest


class AvailabilityGradeCalculation:

    def __init__(self, prometheus):
        self.prometheusRequest = PrometheusRequest.PrometheusRequest(prometheus)
        self.uptimeGrade = 0
        self.uptimeWeight = 1

    def calculateGrade(self):

        return self.uptimeWeight * self.uptimeGrade

    def calculateUptimeGrade(self):
        counter = 1
        uptimeGrade = []
        uptimeValues = self.prometheusRequest.makeRequest("uptime")

        # time = seconds, uptime values = milliseconds
        # denominator to milliseconds so that actualTime and uptimeGrade have the same unit of time
        for x in range(len(uptimeValues) - 1):
            # uptimeGrade = (uptimeGrade - pastUptimeGrade) / ((actualTime - pastTime)*1000)
            uptimeGrade.append((int(uptimeValues[counter][1]) - int(uptimeValues[counter - 1][1])) / (
                    (uptimeValues[counter][0] - uptimeValues[counter - 1][0]) * 1000))
            counter += 1

        self.uptimeGrade = sum(uptimeGrade) / len(uptimeGrade)

    def update(self):
        self.calculateUptimeGrade()

    def initialCalculation(self):
        self.calculateUptimeGrade()
