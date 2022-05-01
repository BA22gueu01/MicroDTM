import subprocess


class DBRequest:

    def makeRequest(self, tableName):
        mysqlCommand = "'select * from tag;'"
        request = subprocess.Popen(["kubectl", "exec", "-n", "sock-shop", "catalogue-db-86c68f4757-4tvzt",
                                   "--container", "catalogue-db", "--", "bash", "-c",
                                   "mysql -u catalogue_user -pdefault_password socksdb -e 'select * from tag;'"], stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
        print("Opened")
        print(request.stdout.readlines())

