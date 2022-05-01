import subprocess


class DBRequest:

    def makeRequest(self, podName, containerName, tableName):
        mysqlCommand = "mysql -u catalogue_user -pdefault_password socksdb -e 'select * from " + tableName + ";'"
        request = subprocess.Popen(["kubectl", "exec", "-n", "sock-shop", podName,
                                   "--container", containerName, "--", "bash", "-c", mysqlCommand],
                                   stdout=subprocess.PIPE)

        answer = []

        if tableName == "tag":
            request.stdout.readline()
            for line in request.stdout.readlines():
                line = line.decode().strip('\n')
                cells = line.split("\t")
                answer.append(cells[1])
        else:
            header = request.stdout.readline()
            header = header.decode().strip('\n')
            headers = header.split("\t")
            headers[0] = "id"
            if tableName == sock:
                headers.remove("image_url_1")
            for line in request.stdout.readlines():
                line = line.decode().strip('\n')
                cells = line.split("\t")
                jsonLine = ""
                for x in range(len(headers) - 1):
                    jsonLine = jsonLine + headers[x] + ":" + cells[x] + ","
                answer.append(jsonLine)

        return answer

