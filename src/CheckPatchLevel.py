import subprocess
import platform
import re
from datetime import timedelta, datetime


class CheckPatchLevel:

    def checkPatchLevel(self):
        try:
            counterInst = 0
            counterSec = 0

            print("Platform: ", platform.linux_distribution())
            # Get the os version of the pod
            version = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf",
                                               "--", "cat", "/etc/os-release"])
            version = version.decode()
            currentVersion = False

            if 'ubuntu' in version.lower() or 'debian' in version.lower():
                if 'ubuntu' in version.lower() and ("20" in version or "18" in version) or \
                        'debian' in version.lower() and ("11" in version or "10" in version):
                    currentVersion = True
                packageManager = "apt-get"
            elif 'alpine' in version.lower():
                if "20" in version or "18" in version:
                    currentVersion = True
                packageManager = "apk"
            else:
                return 0

            # Run the equivalent of apt-get update - fetch the latest list of available packages from the repositories
            subprocess.check_output(
                ["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", packageManager, "update"])

            # Check number of pending updates. -s = No action; perform a simulation of events that would occur based
            # on the current system state but do not actually change the system
            pendingUpdates = subprocess.check_output(
                ["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", packageManager, "-s",
                 "upgrade"])

            pendingUpdates = pendingUpdates.decode()

            if 'ubuntu' in version.lower() or 'debian' in version.lower():
                if 'inst' in pendingUpdates.lower():
                    counterInst += 1
                if 'security' in pendingUpdates.lower():
                    counterSec += 1
            elif 'alpine' in version.lower():
                try:
                    counterInst = re.search(r"(/([0-9]|[1-9][0-9]|[1-9][0-9][0-9]))", pendingUpdates).group(1)
                except AttributeError:
                    counterInst = 9999

            # Check last time since the system was updated
            lastUpdateFile = subprocess.check_output(
                ["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", "ls", "-l",
                 "/var/lib/" + packageManager[0 - 2] + "/"])
            lastUpdateFile = lastUpdateFile.decode()

            if 'update-success-stamp' in lastUpdateFile.lower():
                lastUpdate = subprocess.check_output(
                    ["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", "ls", "-l",
                     "/var/lib/" + packageManager[0 - 2] + "/update-success-stamp"])
                lastUpdate = lastUpdate.decode()

                # To Do: "awk", "'{print $6" "$7" "$8}'"

                currentDate = datetime.datetime.now()

                lastUpdate = currentDate.date().strftime("%Y") + " " + lastUpdate
                lastUpdate = datetime.datetime.strptime(lastUpdate, "%Y %b %d %H:%M")
            else:
                lastUpdate = 0

            print("Version: ", version)
            print("Number of pending updates: ", counterInst)
            print("Number of pending security updates: ", counterSec)
            print("Last time the system was updated: ", lastUpdate)

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
