

class CorrectnessGradeCalculation:

    def __init__(self):
        self.callCorrectnessGrade = 0
        self.callCorrectnessWeight = 1


    def calculateGrade(self):
        return self.callCorrectnessWeight * self.callCorrectnessGrade

    def calculateCallCorrectnessGrade(self):
        self.callCorrectnessGrade = 0
        print("callCorrectnessGrade: ", self.callCorrectnessGrade)

    def hourlyUpdate(self):
        self.calculateCallCorrectnessGrade()

    def initialCalculation(self):
        self.calculateCallCorrectnessGrade()
