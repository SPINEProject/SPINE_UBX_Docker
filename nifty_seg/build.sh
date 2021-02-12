#!/bin/bash

cd "${0%/*}"
docker build -t spine_ubx_niftyseg .
docker tag slicer micheletgregory/spine_ubx_niftyseg:1.0
docker push micheletgregory/spine_ubx_niftyseg:1.0
