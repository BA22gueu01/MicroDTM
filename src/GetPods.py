import subprocess


class GetPods:

    def getPods(self):

        pods = []
        output = subprocess.Popen(["kubectl", "get", "pods", "-n", "sock-shop", "--no-headers",
                                            "--field-selector=status.phase=Running", "-o",
                                            "custom-columns=:metadata.name"], stdout=subprocess.PIPE)
        # output.wait()
        print("POPEN")
        for line in output.stdout.readlines():
            line = line.decode()
            print(line)
            pods.append(line)

        return pods

    def getContainers(podName):
        containers = []
        output = subprocess.Popen(["kubectl", "describe", "pod/"+podName, "-n", "sock-shop"], stdout=subprocess.PIPE)
        output.wait()
        for line in output.stdout.readlines():
            print(line)
            containers.append(line)

        return containers
