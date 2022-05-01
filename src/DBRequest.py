import subprocess
import pexpect


class DBRequest:

    def makeRequest(self, tableName):
        request = pexpect.spawn('kubectl exec -n sock-shop catalogue-db-86c68f4757-4tvzt --container catalogue-db -- /bin/bash')
        print(request.read())
        request.sendline('mysql -u catalogue_user -p \n')
        print(request.read())
        request.expect("Enter password:")
        request.sendline('default_password')
        print(request.read())
        request.sendline('USE socksdb;')
        print(request.read())
        request.sendline('select * from ' + tableName + ';')
        print(request.read())
        request.sendline('exit')
        request.sendline('exit')



