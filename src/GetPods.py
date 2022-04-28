import subprocess

class GetPods:

    def getPods(self):
        pods = []
        output = subprocess.Popen(["kubectl", "get", "pods", "-o", "custom-columns=\":metadata.name\"", "--no-headers",
                                   "--field-selector=status.phase=Running", "-n", "sock-shop"], stdout=subprocess.PIPE)
        output.wait()
        print(output)
        print(output.stdout)
        for line in output.stdout.readlines():
            print(line)
            print(line.decode())
            pods.append(line)

        return pods

    def getContainers(podName):
        containers = []
        output = subprocess.Popen(["kubectl", "describe", "pod/"+podName, "-n", "sock-shop"], stdout=subprocess.PIPE)
        output.wait()
        for line in output.stdout.readlines():
            containers.append(line)

        return containers
