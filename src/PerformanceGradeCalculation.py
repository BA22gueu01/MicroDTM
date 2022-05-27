import PrometheusRequest
import numpy


class PerformanceGradeCalculation:

    def __init__(self, prometheus, updateInterval, historicData):
        self.prometheusRequest = PrometheusRequest.PrometheusRequest(prometheus, updateInterval, historicData)
        self.responseTimeGrades = numpy.zeros(historicData)
        self.responseTimeWeight = 0.4
        self.memoryUsageGrades = numpy.zeros(historicData)
        self.memoryUsageWeight = 0.2
        self.diskReadGrades = numpy.zeros(historicData)
        self.diskReadWeight = 0.1
        self.diskWriteGrades = numpy.zeros(historicData)
        self.diskWriteWeight = 0.1
        self.cpuUsageGrades = numpy.zeros(historicData)
        self.cpuUsageWeight = 0.2

    def calculateGrade(self):

        return (self.responseTimeWeight * numpy.average(self.responseTimeGrades) + self.memoryUsageWeight * numpy.average(self.memoryUsageGrades)
                + self.diskReadWeight * numpy.average(self.diskReadGrades) + self.diskWriteWeight * numpy.average(self.diskWriteGrades)
                + self.cpuUsageWeight * numpy.average(self.cpuUsageGrades))

    def getResponseTimeGrade(self):
        return numpy.average(self.responseTimeGrades)

    def getMemoryUsageGrade(self):
        return numpy.average(self.memoryUsageGrades)

    def getDiskReadGrade(self):
        return numpy.average(self.diskReadGrades)

    def getDiskWriteGrade(self):
        return numpy.average(self.diskWriteGrades)

    def getCpuUsageGrade(self):
        return numpy.average(self.cpuUsageGrades)

    def getSingleResponseTimeGrade(self):
        return self.responseTimeGrades[0]

    def getSingleMemoryUsageGrade(self):
        return self.memoryUsageGrades[0]

    def getSingleDiskReadGrade(self):
        return self.diskReadGrades[0]

    def getSingleDiskWriteGrade(self):
        return self.diskWriteGrades[0]

    def getSingleCpuUsageGrade(self):
        return self.cpuUsageGrades[0]

    def calculateResponseTimeGrade(self, value):
        responseTime = value[1]
        responseTime = float(responseTime)

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

        if diskUsage > 50:
            grade = -5
        elif diskUsage > 25:
            grade = 0
        else:
            grade = 5
        return grade

    def calculateCpuUsageGrade(self, cpuUsage):
        if cpuUsage == [0, 0]:
            grade = 0

        else:
            cpuUsage = float(cpuUsage[0][1]) * 100

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

        cpuUsageValues = self.prometheusRequest.makeRequest('container_spec_cpu_quota')
        self.calculateCpuUsageGrade(cpuUsageValues)

    def initialCalculation(self):
        responseTimeValues = self.prometheusRequest.makeRequest('response_time_history')
        self.subGradeCalculation(responseTimeValues, self.calculateResponseTimeGrade, self.responseTimeGrades, "Response Time Grade: ")

        memoryUsageValues = self.prometheusRequest.makeRequest('memory_usage_history')
        self.subGradeCalculation(memoryUsageValues, self.calculateMemoryUsageGrade, self.memoryUsageGrades, "Memory Usage Grade: ")

        diskReadUsageValues = self.prometheusRequest.makeRequest('disk_read_history')
        self.subGradeCalculation(diskReadUsageValues, self.calculateDiskGrade, self.diskReadGrades, "Disk Read Grade: ")

        diskWriteUsageValues = self.prometheusRequest.makeRequest('disk_write_history')
        self.subGradeCalculation(diskWriteUsageValues, self.calculateDiskGrade, self.diskWriteGrades, "Disk Write Grade: ")

        cpuUsageValues = self.prometheusRequest.makeRequest('container_spec_cpu_quota_history')
        self.calculateCpuUsageGrade(cpuUsageValues)

    def subGradeCalculation(self, values, func, gradeArray, gradeName):
        if values == [0, 0]:
            grade = 0
            self.addNewGrade(grade, gradeArray)
            print(gradeName, grade)

        else:
            length = 0
            for value in values:
                if len(value) > length:
                    length = len(value)

            for x in range(length - 1):
                grade = 0
                counter = 0
                for y in range(len(values)):
                    if x < len(values[y]):
                        grade = grade + func(values[y][x])
                        counter = counter + 1
                grade = grade / counter
                self.addNewGrade(grade, gradeArray)
                print(gradeName, grade)
