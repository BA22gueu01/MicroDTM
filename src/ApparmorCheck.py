import subprocess


class ApparmorCheck:

    def checkApparmor(self):

        output = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", "cat", "/sys/module/apparmor/parameters/enabled"])
        output = output.decode()
        print(output)
        #output = "Y"
        if 'Y' in output:
            return 5
        else:
            return -5
