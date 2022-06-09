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

        if countPods == 0:
            print("ERROR: No Pods found ", pods)
            return 0

        else:
            return grade/countPods

    def checkPatchLevel(self, podName, containerName):

        counterInst = 0
        counterSec = 0
        currentDate = datetime.now()
        neverUpdated = True
        currentVersion = False

        try:
            # Get the os version of the pod
            version = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", podName, "--container",
                                               containerName, "--", "cat", "/etc/os-release"])
            version = version.decode()

            if 'ubuntu' in version.lower() or 'debian' in version.lower():
                if 'ubuntu' in version.lower() and ("20" in version or "18" in version) or \
                        'debian' in version.lower() and ("11" in version or "10" in version):
                    currentVersion = True
                packageManager = "apt-get"
            elif 'alpine' in version.lower():
                if "3.13" in version or "3.14" in version or "3.15" in version:
                    currentVersion = True
                packageManager = "apk"
            else:
                return 0

            try:
                # Run the equivalent of apt-get update - fetch the latest list of available packages from the
                # repositories
                subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", podName, "--container", containerName,
                                         "--", packageManager, "update"], stderr=subprocess.DEVNULL)

                # Check number of pending updates. -s = No action; perform a simulation of events that would occur based
                # on the current system state but do not actually change the system
                pendingUpdates = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", podName, "--container",
                                                          containerName, "--", packageManager, "-s", "upgrade"],
                                                          stderr=subprocess.DEVNULL)
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
                     "/var/lib/" + packageManager[0:3] + "/"], stderr=subprocess.DEVNULL)
                lastUpdateFile = lastUpdateFile.decode()

                if 'update-success-stamp' in lastUpdateFile.lower():
                    neverUpdated = False
                    lastUpdate = subprocess.check_output(
                        ["kubectl", "exec", "-n", "sock-shop", podName, "--container", containerName, "--", "ls", "-l",
                         "/var/lib/" + packageManager[0:3] + "/periodic/update-success-stamp"],
                        stderr=subprocess.DEVNULL)
                    lastUpdate = lastUpdate.decode()

                    columns = lastUpdate.strip().split()
                    lastUpdate = columns[6] + " " + columns[7] + " " + columns[8]
                    print(lastUpdate)

                    lastUpdate = currentDate.date().strftime("%Y") + " " + lastUpdate
                    lastUpdate = datetime.strptime(lastUpdate, "%Y %b %d %H:%M")

            except Exception:
                print("Read-only filesystem or permission denied")

        except Exception:
            currentVersion = False
            counterInst = 0
            counterSec = 0
            currentDate = datetime.now()

        if currentVersion:
            if counterInst < 50 and counterSec < 20:
                if not neverUpdated and (lastUpdate > (currentDate - timedelta(days=90))):
                    return 5
                else:
                    return 2.5
            else:
                return -2.5
        else:
            return -5
