import subprocess

class GetPods:

    def getPods(self):
        pods = []
        output = subprocess.check_output(["kubectl", "get", "pods", "-o=wide",
                                          "-n", "sock-shop"])
        print("Simple Call\n")
        print(output)
        output = output.decode()
        print("Decoded")
        print(output)

        output = subprocess.check_output(["kubectl", "get", "pods", "-o=wide",
                                          "-n", "sock-shop", "--no-headers"])
        print("No Header\n")
        print(output)

        output = subprocess.check_output(["kubectl", "get", "pods", "-o=wide",
                                          "-n", "sock-shop", "--field-selector=status.phase=Running"])
        print("Field Selector\n")
        print(output)

        output = subprocess.check_output(["kubectl", "get", "pods", "-o", "custom-columns=\":metadata.name\"",
                                          "-n", "sock-shop"])
        print("o changed\n")
        print(output)



        return pods

    def getContainers(podName):
        containers = []
        output = subprocess.Popen(["kubectl", "describe", "pod/"+podName, "-n", "sock-shop"], stdout=subprocess.PIPE)
        output.wait()
        for line in output.stdout.readlines():
            containers.append(line)

        return containers
