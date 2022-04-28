import subprocess

class GetPods:

    def getPods(self):
        pods = []
        output = subprocess.check_output(["kubectl", "get", "pods", "-n", "sock-shop", "--no-headers",
                                          "--field-selector=status.phase=Running",  "-o=wide"])
        print("Simple Call\n")
        print(output)
        output = output.decode()
        print("Decoded")
        print(output)

        output = subprocess.check_output(["kubectl", "get", "pods", "-n", "sock-shop", "--no-headers",
                                          "--field-selector=status.phase=Running",  "-o", "custom-columns=:metadata.name"])

        print("Custom\n")
        print(output)

        output = subprocess.check_output(["kubectl", "get", "pods", "-n", "sock-shop", "--no-headers",
                                          "--field-selector=status.phase=Running",  "-o=name"])

        print("Name\n")
        print(output)


        return pods

    def getContainers(podName):
        containers = []
        output = subprocess.Popen(["kubectl", "describe", "pod/"+podName, "-n", "sock-shop"], stdout=subprocess.PIPE)
        output.wait()
        for line in output.stdout.readlines():
            containers.append(line)

        return containers
