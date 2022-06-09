import subprocess
import GetPods


class LogLevelCheck:

    def getLogLevelCount(self):
        getPods = GetPods.GetPods()
        pods = getPods.getPods()
        errorCount = 0
        countPods = 0

        for pod in pods:
            countContainers = 0
            podErrors = 0
            containers = getPods.getContainers(pod)

            for container in containers:
                podErrors = podErrors + self.checkLoglevel(pod, container)
                countContainers = countContainers + 1

            errorCount = errorCount + podErrors / countContainers
            countPods = countPods + 1

        if countPods == 0:
            print("ERROR: No Pods found ", pods)
            return 0

        else:
            return errorCount / countPods

    def checkLoglevel(self, podName, containerName):

        try:
            output = subprocess.check_output(["kubectl", "logs", podName, "--container", containerName,
                                              "--namespace=sock-shop", "--v=1"])
            output = output.decode()
            logLevels = ['warn', 'warning', 'error', 'critical', 'alert', 'fatal', 'emergency']
            counter = 0

            # https://pencilprogrammer.com/check-multiple-substrings-python/
            for x in logLevels:
                if x.lower() in output.lower():
                    counter += 1
        except Exception as e:
            counter = 25
            print(e)
        return counter
