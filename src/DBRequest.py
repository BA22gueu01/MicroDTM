import subprocess


class DBRequest:

    def makeRequest(self, podName, containerName, tableName):
        mysqlCommand = "mysql -u catalogue_user -pdefault_password socksdb -e 'select * from " + tableName + ";'"
        request = subprocess.Popen(["kubectl", "exec", "-n", "sock-shop", podName,
                                   "--container", containerName, "--", "bash", "-c", mysqlCommand],
                                   stdout=subprocess.PIPE)
        answer = []
        for line in request.stdout.readlines():
            line = line.decode().strip('\n')
            print(line)
            answer.append(line)

        return answer

