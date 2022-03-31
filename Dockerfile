FROM python:3.9

RUN mkdir -p /var/TrustCalculation

WORKDIR /var/TrustCalculation

COPY ./ /var/TrustCalculation

RUN pip install -r requirements.txt

ENTRYPOINT python /var/TrustCalculation/src/main.py