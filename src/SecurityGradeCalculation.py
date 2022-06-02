import ApparmorCheck
import CertificateCheck
import VulnerabilityScanCheck


class SecurityGradeCalculation:

    def __init__(self):
        self.apparmorGrade = 0
        self.apparmorWeight = 0.2
        self.certificateGrade = 0
        self.certificateWeight = 0.4
        self.vulnerabilityScanGrade = 0
        self.vulnerabilityScanWeight = 0.4

    def calculateGrade(self):
        return self.apparmorWeight * self.apparmorGrade + self.certificateWeight * self.certificateGrade + self.vulnerabilityScanWeight * self.vulnerabilityScanGrade

    def getAppArmorGrade(self):
        return self.apparmorGrade

    def getCertificateGrade(self):
        return self.certificateGrade

    def getVulnerabilityScanGrade(self):
        return self.vulnerabilityScanGrade

    def calculateVulnerabilityScanGrade(self):
        vulnerabilityScan = VulnerabilityScanCheck.VulnerabilityScan()
        self.vulnerabilityScanGrade = vulnerabilityScan.getVulnerabilityScanGrade()
        print("VulnerabilityScanGrade: ", self.vulnerabilityScanGrade)

    def calculateApparmorGrade(self):
        apparmorCheck = ApparmorCheck.ApparmorCheck()
        self.apparmorGrade = apparmorCheck.getApparmorGrade()
        print("ApparmorGrade: ", self.apparmorGrade)

    def calculateCertificateGrade(self):
        certificateCheck = CertificateCheck.CertificateCheck("zhaw.ch", "443")
        self.certificateGrade = certificateCheck.checkCertificate()
        print("CertificateGrade: ", self.certificateGrade)

    def dailyUpdate(self):
        self.calculateCertificateGrade()
        self.calculateApparmorGrade()
        self.calculateVulnerabilityScanGrade()

    def initialCalculation(self):
        self.calculateCertificateGrade()
        self.calculateApparmorGrade()
        self.calculateVulnerabilityScanGrade()
