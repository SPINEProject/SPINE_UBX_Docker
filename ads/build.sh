#!/bin/bash

# Before running this script you have to download ADS 1.2 and put it in the same folder as this script and dockerfile.

docker build -t ads .
docker tag ads micheletgregory/ads:1.2-ubuntu_jammy-python3.7.7
docker push micheletgregory/ads:1.2-ubuntu_jammy-python3.7.7
