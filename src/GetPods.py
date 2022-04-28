import subprocess


class GetPods:

    def getPods(self):

        pods = []
        output = subprocess.Popen(["kubectl", "get", "pods", "-n", "sock-shop", "--no-headers",
                                            "--field-selector=status.phase=Running", "-o",
                                            "custom-columns=:metadata.name"], stdout=subprocess.PIPE)
        for line in output.stdout.readlines():
            line = line.decode().strip('\n')
            pods.append(line)

        return pods

    def getContainers(self, podName):
        containers = []

        output = subprocess.check_output(["kubectl", "get", "pods", podName, "-o", "jsonpath=\"{.spec.containers[*].name}\"",
                                   "-n", "sock-shop"])

        for line in output.decode().split():
            containers.append(line.strip('"'))

        return containers
