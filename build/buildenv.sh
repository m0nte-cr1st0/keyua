#!/bin/sh
echo Creating environment
virtualenv -p python3 env

echo Install PIP inside virtual environment
./env/bin/easy_install pip

echo Installing dependiencies
./env/bin/pip --no-cache-dir install -r ./build/requirements.txt