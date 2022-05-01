import APIRequest
import DBRequest
import GetPods

class CorrectnessGradeCalculation:

    def __init__(self, sockshop):
        self.callCorrectnessGrade = 0
        self.callCorrectnessWeight = 1
        self.apiRequest = APIRequest.APIRequest(sockshop)
        self.dbRequest = DBRequest.DBRequest()
        self.getPods = GetPods.GetPods()

    def calculateGrade(self):
        return self.callCorrectnessWeight * self.callCorrectnessGrade

    def calculateCallCorrectnessGrade(self):
        self.calculateCatalogueCorrectness()
        self.callCorrectnessGrade = 0
        print("callCorrectnessGrade: ", self.callCorrectnessGrade)

    def calculateCatalogueCorrectness(self):
        pods = self.getPods.getPods()
        podName = ""
        containerName = ""

        for pod in pods:
            if "catalogue-db" in pod and "db" in pod:
                podName = pod
                print(podName)

        containers = self.getPods.getContainers(podName)

        for container in containers:
            print(container)
            containerName = container

        dbAnswer = self.dbRequest.makeRequest(podName, containerName, "tag")
        apiAnswer = self.apiRequest.makeRequest("tags")
        grade = self.getCallGrade(apiAnswer, dbAnswer)
        dbAnswer = self.dbRequest.makeRequest(podName, containerName, "socks")
        apiAnswer = self.apiRequest.makeRequest("catalogue")
        grade = grade + self.getCallGrade(apiAnswer, dbAnswer)

    def getCallGrade(self, apiAnswer, dbAnswer):
        print(len(apiAnswer))
        print(len(dbAnswer))

        if not len(apiAnswer) == len(dbAnswer):
            return -5

        for name in apiAnswer:
            if name not in dbAnswer:
                return -5

        return 5

    def hourlyUpdate(self):
        self.calculateCallCorrectnessGrade()

    def initialCalculation(self):
        self.calculateCallCorrectnessGrade()
