#!/bin/sh

# install smbus lib
apt update -qq && apt install -q --yes python3-smbus
if [ $? -ne 0 ]; then
    echo "Error installing python3-smbus package"
    exit 1
fi

# install Four Letter pHAT driver from Pimoroni
python3 -m pip install --trusted-host pypi.org "fourletterphat>=0.1.0"
if [ $? -ne 0 ]; then
    echo "Error installing Four Letter pHAT driver"
    exit 1
fi

