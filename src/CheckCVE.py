import subprocess
from datetime import timedelta, datetime

class CheckCVE:

    def checkCVE(self):


        imgs = subprocess.check_output(["kubectl", "get", "pods", "-n", "sock-shop"])
        #print(imgs)
        #result = subprocess.check_output(["trivy", "-q", "image", "--light", "--no-progress", "--severity", "CRITICAL", "sock-shop\queue-master-fc75dcdd6-jd7h2"])
        #print(result)
        return 0