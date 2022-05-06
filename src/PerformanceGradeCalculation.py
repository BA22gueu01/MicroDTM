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
        responseTime = float(responseTime)
        print(responseTime)

        if responseTime > 1:
            grade = -5
        elif responseTime >= 0.5:
            grade = 0
        else:
            grade = 5

        return grade

    def calculateMemoryUsageGrade(self, value):
        memoryUsage = value[1]
        memoryUsage = float(memoryUsage) * 100
        print(memoryUsage)

        if memoryUsage > 85:
            grade = -5
        elif memoryUsage > 70:
            grade = 0
        else:
            grade = 5
        return grade

    def calculateDiskGrade(self, value):
        diskUsage = value[1]
        # seconds to ms
        diskUsage = float(diskUsage) * 1000
        print(diskUsage)

        if diskUsage > 50:
            grade = -5
        elif diskUsage > 25:
            grade = 0
        else:
            grade = 5
        return grade

    def calculateCpuUsageGrade(self, cpuUsage):
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
        length = len(grades) - 1
        for x in range(length):
            grades[x] = grades[x + 1]
        grades[length] = newGrade

    def update(self):
        responseTimeValues = self.prometheusRequest.makeRequest('response_time')
        self.subGradeCalculation(responseTimeValues, self.calculateResponseTimeGrade, self.responseTimeGrades, "Response Time Grade: ")

        memoryUsageValues = self.prometheusRequest.makeRequest('memory_usage')
        self.subGradeCalculation(memoryUsageValues, self.calculateMemoryUsageGrade, self.memoryUsageGrades, "Memory Usage Grade: ")

        diskReadUsageValues = self.prometheusRequest.makeRequest('disk_read')
        self.subGradeCalculation(diskReadUsageValues, self.calculateDiskGrade, self.diskReadGrades, "Disk Read Grade: ")

        diskWriteUsageValues = self.prometheusRequest.makeRequest('disk_write')
        self.subGradeCalculation(diskWriteUsageValues, self.calculateDiskGrade, self.diskWriteGrades, "Disk Write Grade: ")

        cpuUsageValues = self.prometheusRequest.makeRequest('container_spec_cpu_quota')[0]
        self.calculateCpuUsageGrade(cpuUsageValues[1])

    def initialCalculation(self):
        responseTimeValues = self.prometheusRequest.makeRequest('response_time_history')
        self.subGradeCalculation(responseTimeValues, self.calculateResponseTimeGrade, self.responseTimeGrades, "Response Time Grade: ")

        memoryUsageValues = self.prometheusRequest.makeRequest('memory_usage_history')
        self.subGradeCalculation(memoryUsageValues, self.calculateMemoryUsageGrade, self.memoryUsageGrades, "Memory Usage Grade: ")

        diskReadUsageValues = self.prometheusRequest.makeRequest('disk_read_history')
        self.subGradeCalculation(diskReadUsageValues, self.calculateDiskGrade, self.diskReadGrades, "Disk Read Grade: ")

        diskWriteUsageValues = self.prometheusRequest.makeRequest('disk_write_history')
        self.subGradeCalculation(diskWriteUsageValues, self.calculateDiskGrade, self.diskWriteGrades, "Disk Write Grade: ")

        cpuUsageValues = self.prometheusRequest.makeRequest('container_spec_cpu_quota_history')[0]
        self.calculateCpuUsageGrade(cpuUsageValues[1])

    def subGradeCalculation(self, values, func, gradeArray, gradeName):
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
