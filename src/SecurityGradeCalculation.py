import ApparmorCheck
import CertificateCheck


class SecurityGradeCalculation:

    def __init__(self):
        self.apparmorGrade = 0
        self.apparmorWeight = 0.4
        self.certificateGrade = 0
        self.certificateWeight = 0.6

    def calculateGrade(self):
        return self.apparmorWeight * self.apparmorGrade + self.certificateWeight * self.certificateGrade

    def calculateApparmorGrade(self):
        apparmorCheck = ApparmorCheck.ApparmorCheck()
        self.apparmorGrade = apparmorCheck.getApparmorGrade()

    def calculateCertificateGrade(self):
        certificateCheck = CertificateCheck.CertificateCheck("zhaw.ch", "443")
        self.certificateGrade = certificateCheck.checkCertificate()

    def dailyUpdate(self):
        self.calculateCertificateGrade()
        self.calculateApparmorGrade()

    def initialCalculation(self):
        self.calculateCertificateGrade()
        self.calculateApparmorGrade()
