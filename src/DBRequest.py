import subprocess


class DBRequest:

    def makeRequest(self, tableName):
        mysqlCommand = "mysql -u catalogue_user -pdefault_password socksdb -e 'select * from" + tableName + ";'"
        request = subprocess.Popen(["kubectl", "exec", "-n", "sock-shop", "catalogue-db-86c68f4757-4tvzt",
                                   "--container", "catalogue-db", "--", "bash", "-c", mysqlCommand],
                                   stdout=subprocess.PIPE)
        answer = []
        for line in request.stdout.readlines():
            line = line.decode().strip('\n')
            answer.append(line)

        return answer

