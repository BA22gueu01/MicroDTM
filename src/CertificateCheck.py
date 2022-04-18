import datetime
import http.client
from urllib.parse import urlparse
from urllib.request import ssl, socket


class CertificateCheck:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def checkURLConnection(self, protocol):
        url = protocol + self.hostname + ":" + self.port
        # https://stackoverflow.com/questions/65955022/python-check-if-webpage-is-http-or-https
        url = urlparse(url)
        conn = http.client.HTTPConnection(url.netloc)
        conn.request("HEAD", url.path)
        if conn.getresponse():
            return True
        else:
            return False

    def checkCertificate(self):
        #
        ### DNS?
        #
        hostname = self.hostname
        port = self.port

        print('Check certificate for: ' + hostname + ":" + port)

        context = ssl.create_default_context()

        # https://github.com/echovue/Operations/blob/master/PythonScripts/TLSValidator.py
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                certificate = ssock.getpeercert()

        certExpires = datetime.datetime.strptime(certificate['notAfter'], '%b %d %H:%M:%S %Y %Z')
        daysToExpiration = (certExpires - datetime.datetime.now()).days

        http = "http://"
        https = "https://"
        if self.checkURLConnection(http):
            if self.checkURLConnection(https):
                if daysToExpiration < 0:
                    return 0
                elif daysToExpiration > 0:
                    return 5
            else:
                return -5
        else:
            # What should we return here?
            return 0
