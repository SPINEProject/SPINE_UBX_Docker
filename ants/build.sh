#!/bin/bash

cd "${0%/*}"
docker build -t spine_ubx_ants .
docker tag slicer micheletgregory/spine_ubx_ants:1.0
docker push micheletgregory/spine_ubx_ants:1.0
