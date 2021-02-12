#!/bin/bash

cd "${0%/*}"
docker build -t spine_ubx_matlab_runtime .
docker tag slicer micheletgregory/spine_ubx_matlab_runtime:1.0
docker push micheletgregory/spine_ubx_matlab_runtime:1.0
