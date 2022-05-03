import PrometheusRequest
import numpy

class PerformanceGradeCalculation:

    def __init__(self, prometheus):
        self.prometheusRequest = PrometheusRequest.PrometheusRequest(prometheus)
        self.responseTimeGrades = numpy.zeros(24)
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

        return (self.responseTimeWeight * numpy.average(self.responseTimeGrades) + self.memoryUsageWeight * numpy.average(self.memoryUsageGrades)
                + self.diskReadWeight * numpy.average(self.diskReadGrades) + self.diskWriteWeight * numpy.average(self.diskWriteGrades)
                + self.cpuUsageWeight * numpy.average(self.cpuUsageGrades))


    def calculateResponseTimeGrade(self, value):
        responseTime = value[1]
        print("responseTime: ", responseTime)
        responseTime = float(responseTime)
        print("responseTime: ", responseTime)

        if responseTime > 1:
            grade = -5
        elif responseTime >= 0.5:
            grade = 0
        else:
            grade = 5

        print("ResponseTimeGrade: ", grade)
        self.addNewGrade(grade, self.responseTimeGrades)

    def calculateMemoryUsageGrade(self, value):
        memoryUsage = value[1]
        print("Memory Usage: ", memoryUsage)
        memoryUsage = float(memoryUsage) * 100

        if memoryUsage > 90:
            grade = -5
        elif memoryUsage > 85:
            grade = 0
        else:
            grade = 5
        print("MemoryUsageGrade: ", grade)
        self.addNewGrade(grade, self.memoryUsageGrades)

    def calculateDiskGrade(self, value):
        diskUsage = value[1]
        print("Disk Usage: ", diskUsage)
        diskUsage = float(diskUsage) * 100

        if diskUsage > 4:
            grade = -5
        elif diskUsage > 2.5:
            grade = 0
        else:
            grade = 5
        return grade

    def calculateCpuUsageGrade(self, value):
        cpuUsage = value[1]
        print(cpuUsage)
        cpuUsage = float(cpuUsage) * 100

        if cpuUsage > 90:
            grade = -5
        elif cpuUsage > 75:
            grade = 0
        else:
            grade = 5
        print("CPU UsageGrade: ", grade)
        self.addNewGrade(grade, self.cpuUsageGrades)

    def addNewGrade(self, newGrade, grades):
        print("uptime Grade: ", newGrade)
        length = len(grades) - 1
        for x in range(length):
            grades[x] = grades[x + 1]
        grades[length] = newGrade

    def update(self):
        responseTimeValues = self.prometheusRequest.makeRequest('memory_usage')
        self.calculateResponseTimeGrade(responseTimeValues[1])

        memoryUsageValues = self.prometheusRequest.makeRequest('memory_usage')
        self.calculateMemoryUsageGrade(memoryUsageValues[1])

        diskReadUsageValues = self.prometheusRequest.makeRequest('disk_read')
        grade = self.calculateDiskGrade(diskReadUsageValues[1])
        print("DiskReadGrade: ", grade)
        self.addNewGrade(grade, self.diskReadGrades)

        diskWriteUsageValues = self.prometheusRequest.makeRequest('disk_write')
        grade = self.calculateDiskGrade(diskWriteUsageValues[1])
        print("DiskWriteGrade: ", grade)
        self.addNewGrade(grade, self.diskWriteGrades)

        cpuUsageValues = self.prometheusRequest.makeRequest('container_spec_cpu_quota')
        self.calculateCpuUsageGrade(cpuUsageValues[1])

    def initialCalculation(self):
        responseTimeValues = self.prometheusRequest.makeRequest('memory_usage_history')
        print(responseTimeValues)
        for value in responseTimeValues:
            print(value)
            self.calculateResponseTimeGrade(value[1])

        memoryUsageValues = self.prometheusRequest.makeRequest('memory_usage_history')
        for value in memoryUsageValues:
            self.calculateMemoryUsageGrade(value)

        diskReadUsageValues = self.prometheusRequest.makeRequest('disk_read_history')
        for value in diskReadUsageValues:
            grade = self.calculateDiskGrade(value)
            print("DiskReadGrade: ", grade)
            self.addNewGrade(grade, self.diskReadGrades)

        diskWriteUsageValues = self.prometheusRequest.makeRequest('disk_write_history')
        for value in diskWriteUsageValues:
            grade = self.calculateDiskGrade(value)
            print("DiskWriteGrade: ", grade)
            self.addNewGrade(grade, self.diskWriteGrades)

        cpuUsageValues = self.prometheusRequest.makeRequest('container_spec_cpu_quota_history')
        for value in cpuUsageValues:
            self.calculateCpuUsageGrade(value)
