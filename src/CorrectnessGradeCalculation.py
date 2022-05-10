import APIRequest
import DBRequest
import GetPods
import numpy


class CorrectnessGradeCalculation:

    def __init__(self, sockshop):
        self.callCorrectnessGrades = numpy.zeros(24)
        self.callCorrectnessWeight = 1
        self.apiRequest = APIRequest.APIRequest(sockshop)
        self.dbRequest = DBRequest.DBRequest()
        self.getPods = GetPods.GetPods()

    def calculateGrade(self):
        return self.callCorrectnessWeight * numpy.average(self.callCorrectnessGrades)

    def getCallCorrectnessGrade(self):
        return numpy.average(self.callCorrectnessGrades)

    def calculateCallCorrectnessGrade(self):
        self.addNewGrade(self.calculateCatalogueCorrectness())

    def calculateCatalogueCorrectness(self):
        pods = self.getPods.getPods()
        podName = ""
        containerName = ""

        for pod in pods:
            if "catalogue-db" in pod and "db" in pod:
                podName = pod

        containers = self.getPods.getContainers(podName)

        for container in containers:
            containerName = container

        dbAnswer = self.dbRequest.makeRequest(podName, containerName, "tag")
        apiAnswer = self.apiRequest.makeRequest("tags")
        grade = self.getCallGrade(apiAnswer, dbAnswer)
        dbAnswer = self.dbRequest.makeRequest(podName, containerName, "sock")
        apiAnswer = self.apiRequest.makeRequest("catalogue")
        grade = grade + self.getCallGrade(apiAnswer, dbAnswer)
        return grade/2

    def getCallGrade(self, apiAnswer, dbAnswer):

        if not len(apiAnswer) == len(dbAnswer):
            return -5

        for name in apiAnswer:
            if name not in dbAnswer:
                return -5

        return 5

    def addNewGrade(self, newGrade):
        print("callCorrectnessGrade: ", newGrade)
        length = len(self.callCorrectnessGrades) - 1
        for x in range(length):
            self.callCorrectnessGrades[x] = self.callCorrectnessGrades[x + 1]
        self.callCorrectnessGrades[length] = newGrade

    def update(self):
        self.calculateCallCorrectnessGrade()

    def initialCalculation(self):
        self.calculateCallCorrectnessGrade()
