#!/bin/bash

set -e

exec python3 /var/TrustCalculation/src/main.py &
exec python3 /var/TrustCalculation/src/Api.py