import subprocess
from datetime import timedelta, datetime

class CheckPatchLevel:

    def checkPatchLevel(self):
        try:
            # Get the ubuntu version of the pod
            #version = subprocess.check_output(["lsb_release", "-a", "|", "grep", "-i", "Description:"])
            version = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", "cat", "/etc/os-release"])
            version = version.decode()
            print("Version: ", version)

            # Run the equivalent of apt-get update - fetch the latest list of available packages from the repositories
            # subprocess.check_output(["sudo", "apt-get", "update"])
            subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", "apt-get", "update"])

            # Check number of pending updates
            # -s = No action; perform a simulation of events that would occur based on the current system state but do not actually change the system
            # pendingUpdates = subprocess.check_output(["sudo", "apt-get", "upgrade", "-s", "|", "grep", "Inst", "|", "wc", "-l"])
            pendingUpdates = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", "apt-get", "upgrade", "-s"])
            pendingUpdates = pendingUpdates.decode()
            counterInst = 0

            if 'inst' in pendingUpdates.lower():
                counterInst += 1
                print("Number of pending updates: ", counterInst)

            # Check number of pending security updates
            # pendingSecurityUpdates = subprocess.check_output(["sudo", "apt-get", "upgrade", "-s", "|", "grep", "Inst", "|", "grep", "security", "|", "wc", "-l"])
            pendingSecurityUpdates = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", "apt-get", "upgrade", "-s"])
            pendingSecurityUpdates = pendingSecurityUpdates.decode()
            counterSec = 0

            if 'security' in pendingSecurityUpdates.lower():
                counterSec += 1
                print("Number of pending security updates: ", counterSec)

            # Check last time since the system was updated
            # lastUpdate = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", "ls", "-l", "/var/lib/apt/periodic/update-success-stamp", "|", "awk", "'{print $6" "$7" "$8}'"])
            lastUpdateFile = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", "ls", "-l", "/var/lib/apt/"])
            lastUpdateFile = lastUpdateFile.decode()

            if 'update-success-stamp' in lastUpdateFile.lower():
                lastUpdate = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", "ls", "-l", "/var/lib/apt/update-success-stamp"])
                lastUpdate = lastUpdate.decode()

                # To Do: "awk", "'{print $6" "$7" "$8}'"

                currentDate = datetime.datetime.now()

                lastUpdate = currentDate.date().strftime("%Y") + " " + lastUpdate
                lastUpdate = datetime.datetime.strptime(lastUpdate, "%Y %b %d %H:%M")
            else:
                lastUpdate = 0

            print("Ubuntu version: ", version)
            print("number of pending updates: ", pendingUpdates)
            print("number of pending security updates: ", pendingSecurityUpdates)
            print("Last time the system was updated: ", lastUpdate)
        except Exception as e:
            print(e)

        if ("ubuntu" in version and ("20" in version or "18" in version)) or ("debian" in version and ("11" in version or "10" in version)):
            if counterInst < 25 and counterSec < 10:
                if lastUpdate > (currentDate - timedelta(days=90)):
                    return 5
            else:
                return 0
        else:
            return -5
