import subprocess
import pexpect


class DBRequest:

    def makeRequest(self, tableName):
        request = pexpect.spawn('kubectl exec -n sock-shop catalogue-db-86c68f4757-4tvzt --container catalogue-db -- /bin/bash -c mysql -u catalogue_user -p')
        print(request.read())
        i = request.expect([pexpect.TIMEOUT, "Enter password:"])





