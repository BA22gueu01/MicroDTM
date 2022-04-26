import subprocess

class LogLevelCheck:

    def checkLoglevel(self):

        try:
            output = subprocess.check_output(["kubectl", "logs", "queue-master-6bf76bbfc-4hcwf", "--container=queue-master", "--namespace=sock-shop", "--v=1",])
            logLevels = ['warning', 'error', 'fatal']
            counter = 0

            # https://pencilprogrammer.com/check-multiple-substrings-python/
            print("output: ", output)
            for x in logLevels:
                if x in output:
                    counter += 1
                    print(counter)
                #subprocess.check_output(["grep", "-i", "-E", "'(warning|error|fatal)'", "|", "wc", "-l"
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