import subprocess
from datetime import timedelta, datetime

class CheckPatchLevel:

    def checkPatchLevel(self):
        # Get the ubuntu version of the pod
        #version = subprocess.check_output(["lsb_release", "-a", "|", "grep", "-i", "Description:"])
        version = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", "lsb_release", "-a", "|", "grep", "-i", "Description:"])

        # Run the equivalent of apt-get update - fetch the latest list of available packages from the repositories
        #subprocess.check_output(["sudo", "apt-get", "update"])
        subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", "sudo", "apt-get", "update"])

        # Check number of pending updates
        # -s = No action; perform a simulation of events that would occur based on the current system state but do not actually change the system
        #pendingUpdates = subprocess.check_output(["sudo", "apt-get", "upgrade", "-s", "|", "grep", "Inst", "|", "wc", "-l"])
        pendingUpdates = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", "sudo", "apt-get", "upgrade", "-s", "|", "grep", "Inst", "|", "wc", "-l"])

        # Check number of pending security updates
        #pendingSecurityUpdates = subprocess.check_output(["sudo", "apt-get", "upgrade", "-s", "|", "grep", "Inst", "|", "grep", "security", "|", "wc", "-l"])
        pendingSecurityUpdates = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", "sudo", "apt-get", "upgrade", "-s", "|", "grep", "Inst", "|", "grep", "security", "|", "wc", "-l"])

        # Check last time since the system was updated
        #lastUpdate = subprocess.check_output(["ls", "-l", "/var/lib/apt/periodic/update-success-stamp", "|", "awk", "'{print $6" "$7" "$8}'"])
        lastUpdate = subprocess.check_output(["kubectl", "exec", "-n", "sock-shop", "queue-master-6bf76bbfc-4hcwf", "--", "ls", "-l", "/var/lib/apt/periodic/update-success-stamp", "|", "awk", "'{print $6" "$7" "$8}'"])
        currentDate = datetime.datetime.now()

        lastUpdate = currentDate.date().strftime("%Y") + " " + lastUpdate
        lastUpdate = datetime.datetime.strptime(lastUpdate, "%Y %b %d %H:%M")

        print("Ubuntu version: ", version)
        print("number of pending updates: ", pendingUpdates)
        print("number of pending security updates: ", pendingSecurityUpdates)
        print("Last time the system was updated: ", lastUpdate)

        if "20" in version or "18" in version:
            if pendingUpdates < 25 and pendingSecurityUpdates < 10:
                if lastUpdate > (currentDate - timedelta(days=90)):
                    return 5
            else:
                return 0
        else:
            return -5
