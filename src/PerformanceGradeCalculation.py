import PrometheusRequest
import numpy

class PerformanceGradeCalculation:

    def __init__(self, prometheus):
        self.prometheusRequest = PrometheusRequest.PrometheusRequest(prometheus)
        self.responseTimeGrade = 0
        self.responseTimeWeight = 0.4
        self.memoryUsageGrades = numpy.zeros(24)
        self.memoryUsageWeight = 0.2
        self.diskReadGrades = numpy.zeros(24)
        self.diskReadWeight = 0.1
        self.diskWriteGrades = numpy.zeros(24)
        self.diskWriteWeight = 0.1
        self.cpuUsageGrades = numpy.zeros(24)
        self.cpuUsageWeight = 0.2

    def calculateGrade(self):

        return (self.responseTimeWeight * self.responseTimeGrade + self.memoryUsageWeight * numpy.average(self.memoryUsageGrades)
                + self.diskReadWeight * numpy.average(self.diskReadGrades) + self.diskWriteWeight * numpy.average(self.diskWriteGrades)
                + self.cpuUsageWeight * numpy.average(self.cpuUsageGrades))

    # Todo What does this metric means? Use historical data
    def calculateResponseTimeGrade(self):
        responseTime = self.prometheusRequest.makeRequest('gauge_response_metrics')[1]
        responseTime = int(responseTime[1])
        print("responseTime: ", responseTime)

        if responseTime > 5:
            self.responseTimeGrade = -5
        elif responseTime > 2.5:
            self.responseTimeGrade = 0
        else:
            self.responseTimeGrade = 5

        print("ResponseTimeGrade: ", self.responseTimeGrade)

    def calculateMemoryUsageGrade(self):
        memoryUsage = self.prometheusRequest.makeRequest('memory_usage')[1]

        memoryUsage = float(memoryUsage) * 100

        if memoryUsage > 90:
            self.memoryUsageGrade = -5
        elif memoryUsage > 85:
            self.memoryUsageGrade = 0
        else:
            self.memoryUsageGrade = 5
        print("MemoryUsageGrade: ", self.memoryUsageGrade)

    def calculateDiskReadGrade(self):
        diskReadUsage = self.prometheusRequest.makeRequest('disk_read')[1]
        diskReadUsage = float(diskReadUsage) * 100

        if diskReadUsage > 4:
            self.diskReadGrade = -5
        elif diskReadUsage > 2.5:
            self.diskReadGrade = 0
        else:
            self.diskReadGrade = 5
        print("DiskReadGrade: ", self.diskReadGrade)

    def calculateDiskWriteGrade(self):
        diskWriteUsage = self.prometheusRequest.makeRequest('disk_write')[1]
        diskWriteUsage = float(diskWriteUsage) * 100

        if diskWriteUsage > 4:
            self.diskWriteGrade = -5
        elif diskWriteUsage > 2.5:
            self.diskWriteGrade = 0
        else:
            self.diskWriteGrade = 5
        print("DiskWriteGrade: ", self.diskWriteGrade)

    def calculateCpuUsageGrade(self):
        cpuUsage = self.prometheusRequest.makeRequest('container_spec_cpu_quota')[1]
        cpuUsage = float(cpuUsage) * 100

        if cpuUsage > 90:
            self.cpuUsageGrade = -5
        elif cpuUsage > 75:
            self.cpuUsageGrade = 0
        else:
            self.cpuUsageGrade = 5
        print("CPU UsageGrade: ", self.cpuUsageGrade)

    def addNewGrade(self, newGrade, grades):
        print("uptime Grade: ", newGrade)
        length = len(grades) - 1
        for x in range(length):
            grades[x] = grades[x + 1]
        grades[length] = newGrade

    def update(self):
        self.calculateResponseTimeGrade()
        self.calculateMemoryUsageGrade()
        self.calculateDiskReadGrade()
        self.calculateDiskWriteGrade()
        self.calculateCpuUsageGrade()
        uptimeValues = self.prometheusRequest.makeRequest("uptime")
        grade = 0
        counter = 0
        for value in uptimeValues:
            grade = grade + self.calculateUptimeGrade(value[0], value[1])
            counter = counter + 1
        grade = grade/counter
        self.addNewGrade(grade)

    def initialCalculation(self):
        print(self.prometheusRequest.makeRequest('memory_usage'))
        print(self.prometheusRequest.makeRequest('memory_usage_history'))
        print(self.prometheusRequest.makeRequest('disk_read'))
        print(self.prometheusRequest.makeRequest('disk_read_history'))
        print(self.prometheusRequest.makeRequest('disk_write'))
        print(self.prometheusRequest.makeRequest('disk_write_history'))
        print(self.prometheusRequest.makeRequest('container_spec_cpu_quota'))
        print(self.prometheusRequest.makeRequest('container_spec_cpu_quota_history'))
        self.calculateResponseTimeGrade()
        self.calculateMemoryUsageGrade()
        self.calculateDiskReadGrade()
        self.calculateDiskWriteGrade()
        self.calculateCpuUsageGrade()
        uptimeValues = self.prometheusRequest.makeRequest("uptime_history")
        length = len(uptimeValues[0]) - 1
        for x in range(length):
            grade = 0
            counter = 0
            for value in uptimeValues:
                grade = grade + self.calculateUptimeGrade(value[x + 1], value[x])
                counter = counter + 1
            grade = grade / counter
            self.addNewGrade(grade)