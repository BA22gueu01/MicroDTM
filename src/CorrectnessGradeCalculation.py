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
        print(self.apiRequest.makeRequest("tags"))
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
        self.dbRequest.makeRequest(podName, containerName, "tag")

    def hourlyUpdate(self):
        self.calculateCallCorrectnessGrade()

    def initialCalculation(self):
        self.calculateCallCorrectnessGrade()
