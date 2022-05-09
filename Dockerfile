FROM python:3.9

RUN mkdir -p /var/TrustCalculation

WORKDIR /var/TrustCalculation

COPY ./ /var/TrustCalculation

# Install kubectl from Docker Hub.
COPY --from=lachlanevenson/k8s-kubectl:v1.10.3 /usr/local/bin/kubectl /usr/local/bin/kubectl

COPY --from=aquasec/trivy:latest /usr/local/bin/trivy /usr/local/bin/trivy

# https://stackoverflow.com/questions/60382570/adding-lets-encrypt-certificates-to-debian9-docker-image
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ca-certificates \
      openssl \
 && mkdir -p /usr/local/share/ca-certificates

# install Let's Encrypt CA Root certificate
ADD https://letsencrypt.org/certs/isrgrootx1.pem.txt /usr/local/share/ca-certificates/isrgrootx1.pem
ADD https://letsencrypt.org/certs/trustid-x3-root.pem.txt /usr/local/share/ca-certificates/trustid-x3-root.pem

# install Let's Encrypt CA Intermediate certificate
ADD https://letsencrypt.org/certs/lets-encrypt-r3.pem /usr/local/share/ca-certificates/lets-encrypt-r3.pem

RUN cd /usr/local/share/ca-certificates \
 && openssl x509 -in isrgrootx1.pem -inform PEM -out isrgrootx1.crt \
 && openssl x509 -in trustid-x3-root.pem -inform PEM -out trustid-x3-root.crt \
 && openssl x509 -in lets-encrypt-r3.pem -inform PEM -out lets-encrypt-r3.crt \
 && update-ca-certificates

RUN pip install -r requirements.txt

RUN ["chmod", "+x", "/var/TrustCalculation/docker_entrypoint.sh"]

ENTRYPOINT [ "bash", "-c", "./docker_entrypoint.sh"]
#ENTRYPOINT python -u /var/TrustCalculation/src/main.py