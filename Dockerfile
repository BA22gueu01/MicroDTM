FROM python:3.9

RUN mkdir -p /var/trustcalc

WORKDIR /var/trustcalc

COPY ./ /var/trustcalc

ENTRYPOINT python /var/trustcalc/main.py