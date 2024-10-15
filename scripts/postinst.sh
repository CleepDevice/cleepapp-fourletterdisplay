#!/bin/sh

# install Four Letter pHAT driver from Pimoroni
python3 -m pip install --trusted-host pypi.org "fourletterphat>=0.1.0" "smbus"
if [ $? -ne 0 ]; then
    echo "Error installing Four Letter pHAT driver"
    exit 1
fi

