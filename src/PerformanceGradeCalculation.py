import PrometheusRequest


class PerformanceGradeCalculation:

    def __init__(self, prometheus):
        self.prometheusRequest = PrometheusRequest.PrometheusRequest(prometheus)
        self.responseTimeGrade = 0
        self.responseTimeWeight = 0.4
        self.memoryUsageGrade = 0
        self.memoryUsageWeight = 0.2
        self.diskReadGrade = 0
        self.diskReadWeight = 0.1
        self.diskWriteGrade = 0
        self.diskWriteWeight = 0.1
        self.cpuUsageGrade = 0
        self.cpuUsageWeight = 0.2

    def calculateGrade(self):

        return (self.responseTimeWeight * self.responseTimeGrade + self.memoryUsageWeight * self.memoryUsageGrade
                + self.diskReadWeight * self.diskReadGrade + self.diskWriteWeight * self.diskWriteGrade
                + self.cpuUsageWeight * self.cpuUsageGrade)

    def calculateResponseTimeGrade(self):
        responseTime = self.prometheusRequest.makeRequest('gauge_response_metrics')[1]
        responseTime = int(responseTime)
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
        print("cpuUsage: ", cpuUsage)

        if cpuUsage > 90:
            self.cpuUsageGrade = -5
        elif cpuUsage > 75:
            self.cpuUsageGrade = 0
        else:
            self.cpuUsageGrade = 5
        print("CPU UsageGrade: ", self.cpuUsageGrade)

    def update(self):
        self.calculateResponseTimeGrade()
        self.calculateMemoryUsageGrade()
        self.calculateDiskReadGrade()
        self.calculateDiskWriteGrade()
        self.calculateCpuUsageGrade()

    def initialCalculation(self):
        self.calculateResponseTimeGrade()
        self.calculateMemoryUsageGrade()
        self.calculateDiskReadGrade()
        self.calculateDiskWriteGrade()
        self.calculateCpuUsageGrade()
