import ApparmorCheck
import CertificateCheck
import VulnerabilityScanCheck
from multiprocessing import Lock


class SecurityGradeCalculation:

    def __init__(self, EXTERN_URL):
        self.lock = Lock()
        self.apparmorGrade = 0
        self.apparmorWeight = 0.2
        self.certificateGrade = 0
        self.certificateWeight = 0.3
        self.vulnerabilityScanGrade = 0
        self.vulnerabilityScanWeight = 0.5
        self.vulnerabilityScan = VulnerabilityScanCheck.VulnerabilityScan()
        self.externUrl = EXTERN_URL
        self.counter = 0

    def calculateGrade(self):
        with self.lock:
            return self.apparmorWeight * self.apparmorGrade + self.certificateWeight * self.certificateGrade + self.vulnerabilityScanWeight * self.vulnerabilityScanGrade

    def getAppArmorGrade(self):
        with self.lock:
            return self.apparmorGrade

    def getCertificateGrade(self):
        with self.lock:
            return self.certificateGrade

    def getVulnerabilityScanGrade(self):
        with self.lock:
            return self.vulnerabilityScanGrade

    def getNiktoCheckGrade(self):
        return self.vulnerabilityScan.getNiktoCheckGrade()

    def getSsllabsCheckGrade(self):
        return self.vulnerabilityScan.getSsllabsCheckGrade()

    def getHttpobsCheckGrade(self):
        return self.vulnerabilityScan.getHttpobsCheckGrade()

    def calculateVulnerabilityScanGrade(self):
        with self.lock:
            counter = self.counter
        grade = self.vulnerabilityScan.getVulnerabilityScanGrade(self.externUrl[counter])
        with self.lock:
            self.vulnerabilityScanGrade = grade
            print("VulnerabilityScanGrade: ", self.vulnerabilityScanGrade)

    def calculateApparmorGrade(self):
        apparmorCheck = ApparmorCheck.ApparmorCheck()
        grade = apparmorCheck.getApparmorGrade()
        with self.lock:
            self.apparmorGrade = grade
            print("ApparmorGrade: ", self.apparmorGrade)

    def calculateCertificateGrade(self):
        certificateCheck = CertificateCheck.CertificateCheck("zhaw.ch", "443")
        grade = certificateCheck.checkCertificate()
        with self.lock:
            self.certificateGrade = grade
            print("CertificateGrade: ", self.certificateGrade)

    def dailyUpdate(self):
        self.calculateCertificateGrade()
        self.calculateApparmorGrade()
        self.calculateVulnerabilityScanGrade()
        with self.lock:
            self.counter = (self.counter + 1) % len(self.externUrl)

    def initialCalculation(self):
        self.calculateCertificateGrade()
        self.calculateApparmorGrade()
        self.calculateVulnerabilityScanGrade()
        with self.lock:
            self.counter = (self.counter + 1) % len(self.externUrl)
