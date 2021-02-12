#!/bin/bash

cd "${0%/*}"
docker build -t spine_ubx .
docker tag slicer micheletgregory/spine_ubx:1.0
docker push micheletgregory/spine_ubx:1.0
