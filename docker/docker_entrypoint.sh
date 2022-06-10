#!/bin/bash

set -e

exec python3 -u /var/TrustCalculation/src/main.py &
exec python3 -u /var/TrustCalculation/src/Api.py