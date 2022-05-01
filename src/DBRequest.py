import subprocess
import pexpect


class DBRequest:

    def makeRequest(self, tableName):
        request = pexpect.spawn('kubectl exec -n sock-shop catalogue-db-86c68f4757-4tvzt --container catalogue-db -- /bin/bash')
        print(request.read())
        request.send('mysql -u catalogue_user -p')
        print(request.read())
        i = request.expect([pexpect.TIMEOUT, "Enter password:"])
        if i == 0:
            print("Got unexpected output: %s %s" % (request.before, request.after))
            request.send(chr(13))
            print(request.read())
            i = request.expect([pexpect.TIMEOUT, "Enter password:"])
            print(i)

        else:
            request.sendline('default_password')
            print(request.read())
            request.sendline('USE socksdb;')
            print(request.read())
            request.sendline('select * from ' + tableName + ';')
            print(request.read())
            request.sendline('exit')
            request.sendline('exit')





