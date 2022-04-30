import subprocess
import GetPods


class ApparmorCheck:

    def getApparmorGrade(self):
        getPods = GetPods.GetPods()
        pods = getPods.getPods()
        grade = 0
        countPods = 0

        for pod in pods:
            countContainers = 0
            podGrade = 0
            containers = getPods.getContainers(pod)

            for container in containers:
                podGrade = podGrade + self.checkApparmor(pod, container)
                countContainers = countContainers + 1

            grade = grade + podGrade/countContainers
            countPods = countPods + 1

        return grade/countPods

    def checkApparmor(self, podName, containerName):

        try:
            output = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", podName, "--container",
                                              containerName, "--", "cat", "/sys/module/apparmor/parameters/enabled"])
            output = output.decode()

        except Exception as e:
            print(e)
            output = "N"

        if 'Y' in output:
            return 5
        else:
            return -5
