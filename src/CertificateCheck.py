import datetime
import http.client
import sys
import os
import re
from socket import socket
from urllib.parse import urlparse
from urllib.request import ssl, socket

import OpenSSL
from OpenSSL import crypto
from oscrypto import tls
from certvalidator import CertificateValidator, errors, ValidationContext
from asn1crypto import pem


class CertificateCheck:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def checkURLConnection(self, protocol):
        url = protocol + self.hostname
        # https://stackoverflow.com/questions/65955022/python-check-if-webpage-is-http-or-https
        url = urlparse(url)
        conn = http.client.HTTPConnection(url.netloc)
        conn.request("HEAD", url.path)
        if conn.getresponse():
            return True
        else:
            return False

    # Download the certificate first for later path validation
    # https://www.codeproject.com/Tips/1278114/Python-3-How-to-download-view-and-save-Certificate
    def downloadCertificateChain(self, host, port):
        s = socket.socket()
        context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_2_METHOD)
        print('Connecting to {0} to get certificate...'.format(host))
        conn = OpenSSL.SSL.Connection(context, s)
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cert')) + '\\'
        certs = []

        try:
            conn.connect((host, int(port)))
            conn.do_handshake()
            certs = conn.get_peer_cert_chain()

        except OpenSSL.SSL.Error as e:
            print('Error: {0}'.format(str(e)))
            exit(1)

        try:
            for index, cert in enumerate(certs):
                cert_components = dict(cert.get_subject().get_components())
                if sys.version_info[0] >= 3:
                    cn = (cert_components.get(b'CN')).decode('utf-8')
                else:
                    cn = cert_components.get('CN')
                print('Certificate {0} - CN: {1}'.format(index, cn))

                try:
                    temp_certname = '{0}_{1}.crt'.format(directory, index)
                    with open(temp_certname, 'w+') as output_file:
                        if sys.version_info[0] >= 3:
                            output_file.write((crypto.dump_certificate
                                               (crypto.FILETYPE_PEM, cert).decode('utf-8')))
                        else:
                            output_file.write((crypto.dump_certificate(crypto.FILETYPE_PEM, cert)))
                except IOError:
                    print('Exception:  {0}'.format(IOError.strerror))

        except OpenSSL.SSL.Error as e:
            print('Error: {0}'.format(str(e)))
            exit(1)

    # https://github.com/wbond/certvalidator/blob/master/docs/usage.md
    def validateEndEntitiyCertificate(self):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'cert')) + '\\_0.crt', 'rb') as f:
            end_entity_cert = f.read()

        try:
            # allow the fetching of CRLs or OCSP responses
            context = ValidationContext(allow_fetching=True)
            validator = CertificateValidator(end_entity_cert, validation_context=context)
            validator.validate_usage(set(['digital_signature']))
            print("The end certificate is valid.")
            return True
        except (errors.PathValidationError, errors.PathBuildingError) as e:
            print("The end certificate could not be validated.")
            print('Error: {0}'.format(str(e)))
            return False

    def validateIntermediateCertificate(self):
        # find and validate intermediate certificate
        # directory iteration:
        # https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cert')) + '/'
        fsdirectory = os.fsencode(directory)
        counter = 0

        # count number of certificates to find out number of intermediate certificates
        for file in os.listdir(fsdirectory):
            filename = os.fsdecode(file)
            if filename.endswith(".crt"):
                counter += 1
                continue
            else:
                continue

        pattern = re.compile(r'[1-' + str(counter - 2) + '].crt')
        intermediateCertificates = []
        for file in os.listdir(fsdirectory):
            filename = os.fsdecode(file)
            if re.search(pattern, filename):
                intermediateCertificates.append(directory + filename)
                continue
            else:
                continue

        # merge intermediate files to one pem file
        with open(directory + 'intermediate.pem', 'w') as outfile:
            for intermediate in intermediateCertificates:
                with open(intermediate, 'r') as infile:
                    outfile.write(infile.read())
                outfile.write("\n")

        end_entity_cert = None
        intermediates = []

        with open(directory + 'intermediate.pem', 'rb') as f:
            for type_name, headers, der_bytes in pem.unarmor(f.read(), multiple=True):
                if end_entity_cert is None:
                    end_entity_cert = der_bytes
                else:
                    intermediates.append(der_bytes)

        try:
            CertificateValidator(end_entity_cert, intermediates)
            print("The intermediate certificate is valid.")
            return True
        except errors.PathValidationError as e:
            print("The certificate could not be validated.")
            print('Error: {0}'.format(str(e)))
            return False

    def checkCertificate(self):
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
        try:
            if self.checkURLConnection(http):
                try:
                    if self.checkURLConnection(https):
                        try:
                            session = tls.TLSSession(manual_validation=True)
                            connection = tls.TLSSocket(hostname, int(port), session=session)
                            try:
                                validator = CertificateValidator(connection.certificate, connection.intermediates)
                                validator.validate_tls(connection.hostname)
                                self.downloadCertificateChain(hostname, port)
                                end_entity_cert_validation = self.validateEndEntitiyCertificate()
                                intermediate_cert_validation = self.validateIntermediateCertificate()
                            except errors.PathValidationError:
                                end_entity_cert_validation = False
                                intermediate_cert_validation = False
                                print("The certificate did not match the hostname, or could not be otherwise validated")
                        except OpenSSL.SSL.Error as e:
                            print('Error: {0}'.format(str(e)))
                            exit(1)

                        if daysToExpiration < 0 and intermediate_cert_validation and end_entity_cert_validation:
                            return 0
                        elif daysToExpiration > 0 and intermediate_cert_validation and end_entity_cert_validation:
                            return 5
                        else:
                            return -5
                    else:
                        return -5
                except ConnectionRefusedError as e:
                    print(e)
                    return -5
            else:
                return 0
        except ConnectionRefusedError as e:
            print(e)
            return 0
