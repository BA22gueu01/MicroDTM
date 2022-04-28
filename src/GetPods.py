import subprocess

class GetPods:

    def getPods(self):
        pods = []
        output = subprocess.Popen(["kubectl", "get", "pods", "-o", "custom-columns=\":metadata.name\"", "--no-headers",
                                   "--field-selector=status.phase=Running", "-n", "sock-shop"], stdout=subprocess.PIPE)
        for line in output.stdout.readlines():
            pods.insert(line)

        return pods

    def getContainers(podName):

        return containers