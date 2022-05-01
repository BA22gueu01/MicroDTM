import subprocess
import pexpect


class DBRequest:

    def makeRequest(self, tableName):
        request = subprocess.Popen('kubectl exec -i -t -n sock-shop catalogue-db-86c68f4757-4tvzt --container catalogue-db '
                                '-- /bin/bash -c "mysql -u catalogue_user -pdefault_password socksdb"', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        print("Opened")
        request.communicate("select * from tag;")
        print(request.stdout.readlines())

