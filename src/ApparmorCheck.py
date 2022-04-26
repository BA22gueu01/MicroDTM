import subprocess


class ApparmorCheck:

    def checkApparmor(self):

        try:
            output = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", "cat", "/sys/module/apparmor/parameters/enabled"])
            output = output.decode()
            print(output)
        except Exception as e:
            print(e)
            output = "N"

        if 'Y' in output:
            return 5
        else:
            return -5
