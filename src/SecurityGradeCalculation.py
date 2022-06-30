import ApparmorCheck
import CertificateCheck
import VulnerabilityScanCheck


class SecurityGradeCalculation:

    def __init__(self, EXTERN_URL, CERTIFICATE_URL):
        self.apparmorGrade = 0
        self.apparmorWeight = 0.2
        self.certificateGrade = 0
        self.certificateWeight = 0.3
        self.vulnerabilityScanGrade = 0
        self.vulnerabilityScanWeight = 0.5
        self.vulnerabilityScan = VulnerabilityScanCheck.VulnerabilityScan()
        self.externUrl = EXTERN_URL
        self.certificateUrl = CERTIFICATE_URL
        self.counter = 0

    def calculateGrade(self):
        return self.apparmorWeight * self.apparmorGrade + self.certificateWeight * self.certificateGrade \
               + self.vulnerabilityScanWeight * self.vulnerabilityScanGrade

    def getAppArmorGrade(self):
        return self.apparmorGrade

    def getCertificateGrade(self):
        return self.certificateGrade

    def getVulnerabilityScanGrade(self):
        return self.vulnerabilityScanGrade

    def getNiktoCheckGrade(self):
        return self.vulnerabilityScan.getNiktoCheckGrade()

    def getSsllabsCheckGrade(self):
        return self.vulnerabilityScan.getSsllabsCheckGrade()

    def getHttpobsCheckGrade(self):
        return self.vulnerabilityScan.getHttpobsCheckGrade()

    def calculateVulnerabilityScanGrade(self):
        self.vulnerabilityScanGrade = self.vulnerabilityScan.getVulnerabilityScanGrade(self.externUrl[self.counter])
        print("VulnerabilityScanGrade: ", self.vulnerabilityScanGrade)

    def calculateApparmorGrade(self):
        apparmorCheck = ApparmorCheck.ApparmorCheck()
        self.apparmorGrade = apparmorCheck.getApparmorGrade()
        print("ApparmorGrade: ", self.apparmorGrade)

    def calculateCertificateGrade(self):
        certificateCheck = CertificateCheck.CertificateCheck(self.certificateUrl, "443")
        self.certificateGrade = certificateCheck.checkCertificate()
        print("CertificateGrade: ", self.certificateGrade)

    def dailyUpdate(self):
        self.calculateCertificateGrade()
        self.calculateApparmorGrade()
        self.calculateVulnerabilityScanGrade()
        self.counter = (self.counter + 1) % len(self.externUrl)

    def initialCalculation(self):
        self.calculateCertificateGrade()
        self.calculateApparmorGrade()
        self.calculateVulnerabilityScanGrade()
        self.counter = (self.counter + 1) % len(self.externUrl)
