import subprocess
from datetime import timedelta, datetime

class CheckCVE:

    def checkCVE(self):


        imgs = subprocess.check_output(["kubectl", "get", "pods", "-n", "sock-shop"])
        print(imgs)
        for img in imgs:
            result = subprocess.check_output(["trivy", "-q", "image", "--light", "--no-progress", "--severity", "CRITICAL", img])
            print(result)
        return 0