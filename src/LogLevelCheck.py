import subprocess

class LogLevelCheck:

    def checkLoglevel(self):

        try:
            output = subprocess.check_output(["kubectl", "logs", "queue-master-6bf76bbfc-4hcwf", "--container=queue-master", "--namespace=sock-shop", "--v=1",])
            #subprocess.check_output(["grep", "-i", "-E", "'(warning|error|fatal)'", "|", "wc", "-l"
            print(output)
        except Exception as e:
            print(e)
            output = 20

        # to be updated
        if output > 25:
            return -5
        elif 25 == output > 10:
            return 0
        else:
            return 5