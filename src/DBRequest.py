import subprocess
import pexpect


class DBRequest:

    def makeRequest(self, tableName):
        request = pexpect.spawn('kubectl exec -i -t -n sock-shop catalogue-db-86c68f4757-4tvzt --container catalogue-db -- /bin/bash -c "mysql -u catalogue_user -pdefault_password socksdb"')
        print(request.read())
