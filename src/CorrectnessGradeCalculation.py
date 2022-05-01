import APIRequest
import DBRequest

class CorrectnessGradeCalculation:

    def __init__(self, sockshop):
        self.callCorrectnessGrade = 0
        self.callCorrectnessWeight = 1
        self.apiRequest = APIRequest.APIRequest(sockshop)
        self.dbRequest = DBRequest.DBRequest()

    def calculateGrade(self):
        return self.callCorrectnessWeight * self.callCorrectnessGrade

    def calculateCallCorrectnessGrade(self):
        print(self.apiRequest.makeRequest("tags"))
        self.dbRequest.makeRequest("tag")
        self.callCorrectnessGrade = 0
        print("callCorrectnessGrade: ", self.callCorrectnessGrade)

    def hourlyUpdate(self):
        self.calculateCallCorrectnessGrade()

    def initialCalculation(self):
        self.calculateCallCorrectnessGrade()
