FROM python:3.9

RUN mkdir -p /var/TrustCalculation

WORKDIR /var/TrustCalculation

COPY ./ /var/TrustCalculation

# Install kubectl from Docker Hub.
COPY --from=lachlanevenson/k8s-kubectl:v1.10.3 /usr/local/bin/kubectl /usr/local/bin/kubectl

COPY --from=aquasec/trivy:latest /usr/local/bin/trivy /usr/local/bin/trivy

RUN pip install -r requirements.txt

RUN ["chmod", "+x", "/var/TrustCalculation/docker_entrypoint.sh"]

ENTRYPOINT [ "bash", "-c", "./docker_entrypoint.sh"]
#ENTRYPOINT python -u /var/TrustCalculation/src/main.py