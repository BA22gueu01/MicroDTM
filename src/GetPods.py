import subprocess

class GetPods:

    def getPods(self):
        pods = []
        output = subprocess.check_output(["kubectl", "get", "pods", "-o", "custom-columns=\":metadata.name\"",
                                          "--no-headers", "--field-selector=status.phase=Running", "-n", "sock-shop"])
        print(output)
        for line in output.decode():
            print(line + "\n")

        return pods

    def getContainers(podName):
        containers = []
        output = subprocess.Popen(["kubectl", "describe", "pod/"+podName, "-n", "sock-shop"], stdout=subprocess.PIPE)
        output.wait()
        for line in output.stdout.readlines():
            containers.append(line)

        return containers
