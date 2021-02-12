#!/bin/bash

cd "${0%/*}"
docker build -t spine_ubx_fsl6 .
docker tag slicer micheletgregory/spine_ubx_fsl6:1.0
docker push micheletgregory/spine_ubx_fsl6:1.0
