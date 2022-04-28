import subprocess
import re
import GetPods
from datetime import timedelta, datetime


class PatchLevelCheck:

    def getPatchLevelGrade(self):
        getPods = GetPods.GetPods()
        pods = getPods.getPods()
        grade = 0
        countPods = 0

        for pod in pods:
            countContainers = 0
            podGrade = 0
            containers = getPods.getContainers(pod)

            for container in containers:
                podGrade = podGrade + self.checkPatchLevel(pod, container)
                countContainers = countContainers + 1

            grade = grade + podGrade/countContainers
            countPods = countPods + 1

        return grade/countPods

    def checkPatchLevel(self, podName, containerName):

        print("PatchLevelCheck for Pod: " + podName + " & container: " + containerName)

        try:
            counterInst = 0
            counterSec = 0

            # Get the os version of the pod
            version = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", podName, "--container",
                                               containerName, "--", "cat", "/etc/os-release"])
            version = version.decode()
            currentVersion = False

            if 'ubuntu' in version.lower() or 'debian' in version.lower():
                if 'ubuntu' in version.lower() and ("20" in version or "18" in version) or \
                        'debian' in version.lower() and ("11" in version or "10" in version):
                    currentVersion = True
                packageManager = "apt-get"
            elif 'alpine' in version.lower():
                if "3.12" in version or "3.13" in version or "3.14" in version or "3.15" in version:
                    currentVersion = True
                packageManager = "apk"
            else:
                return 0

            # Run the equivalent of apt-get update - fetch the latest list of available packages from the repositories
            subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", podName, "--container", containerName,
                                     "--", packageManager, "update"])

            # Check number of pending updates. -s = No action; perform a simulation of events that would occur based
            # on the current system state but do not actually change the system
            pendingUpdates = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", podName, "--container",
                                                      containerName, "--", packageManager, "-s", "upgrade"])
            pendingUpdates = pendingUpdates.decode()

            if 'ubuntu' in version.lower() or 'debian' in version.lower():
                if 'inst' in pendingUpdates.lower():
                    counterInst += 1
                if 'security' in pendingUpdates.lower():
                    counterSec += 1
            elif 'alpine' in version.lower():
                try:
                    # Search for total number of pending updates
                    counterInst = re.search(r"/(\b\d+\b)", pendingUpdates).group(1)
                    if counterInst is None:
                        counterInst = 0
                except AttributeError:
                    return 0

            # Check last time since the system was updated
            lastUpdateFile = subprocess.check_output(
                ["kubectl", "exec", "-n", "sock-shop", podName, "--container", containerName, "--", "ls", "-l",
                 "/var/lib/" + packageManager[0:3] + "/"])
            lastUpdateFile = lastUpdateFile.decode()

            if 'update-success-stamp' in lastUpdateFile.lower():
                lastUpdate = subprocess.check_output(
                    ["kubectl", "exec", "-n", "sock-shop", podName, "--container", containerName, "--", "ls", "-l",
                     "/var/lib/" + packageManager[0:3] + "/periodic/update-success-stamp"])
                lastUpdate = lastUpdate.decode()

                #for line in lastUpdate:
                columns = lastUpdate.strip().split()
                lastUpdate = columns[6] + " " + columns[7] + " " + columns[8]
                print(lastUpdate)

                currentDate = datetime.datetime.now()

                lastUpdate = currentDate.date().strftime("%Y") + " " + lastUpdate
                lastUpdate = datetime.datetime.strptime(lastUpdate, "%Y %b %d %H:%M")
            else:
                lastUpdate = 9999

            print(version)
            print("Is os version up-to-date? ", currentVersion)
            print("Number of pending updates: ", counterInst)
            print("Number of pending security updates: ", counterSec)
            print("Last time the system was updated:")
            print("never" if lastUpdate == 9999 else lastUpdate)

        except Exception as e:
            print(e)

        if currentVersion:
            if counterInst < 50 and counterSec < 20:
                if lastUpdate > (currentDate - timedelta(days=90)):
                    return 5
                else:
                    return 2.5
            else:
                return -2.5
        else:
            return -5
