import subprocess
import sys

class LogLevelCheck:

    def checkLoglevel(self):

        try:
            output = subprocess.check_output(["kubectl", "logs", "queue-master-fc75dcdd6-jd7h2", "--container=queue-master", "--namespace=sock-shop", "--v=1"])#.decode(sys.stdout.encoding).strip()
            output = output.decode()
            logLevels = ['warning', 'error', 'fatal']
            counter = 0

            # https://pencilprogrammer.com/check-multiple-substrings-python/
            for x in logLevels:
                if x.lower() in output.lower():
                    counter += 1
                    print(counter)
        except Exception as e:
            counter = 25
            print(e)

        # to be updated
        if counter > 25:
            return -5
        elif 25 == counter > 10:
            return 0
        else:
            return 5