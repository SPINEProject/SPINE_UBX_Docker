# Use ubuntu xenial as a parent image
FROM ubuntu:xenial

RUN apt-get update

RUN apt-get install curl -y

RUN apt-get install make gcc g++ libx11-dev libxt-dev libgl1-mesa-dev libglu1-mesa-dev libfontconfig-dev libxrender-dev libncurses5-dev -y

#RUN apt-get update && apt-get -y install cmake protobuf-compiler

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install wget unzip xorg
# Install cake
RUN wget https://github.com/Kitware/CMake/releases/download/v3.17.2/cmake-3.17.2-Linux-x86_64.sh \
      -q -O /tmp/cmake-install.sh \
      && chmod u+x /tmp/cmake-install.sh \
      && mkdir /usr/bin/cmake \
      && /tmp/cmake-install.sh --skip-license --prefix=/usr/bin/cmake \
      && rm /tmp/cmake-install.sh

ENV PATH="/usr/bin/cmake/bin:${PATH}"

RUN apt-get install libgstreamer-plugins-base0.10-dev -y

RUN apt install -y git

# add src (it contains dcm2niix if needed)
ADD ./src /src

# Matlab runtime AND SP12
# Install MATLAB MCR in /opt/mcr/
ENV MATLAB_VERSION R2019b
ENV MCR_VERSION v97
RUN mkdir /opt/mcr_install \
 && mkdir /opt/mcr \
 && wget --progress=bar:force -P /opt/mcr_install https://ssd.mathworks.com/supportfiles/downloads/${MATLAB_VERSION}/Release/3/deployment_files/installer/complete/glnxa64/MATLAB_Runtime_${MATLAB_VERSION}_Update_3_glnxa64.zip \
 && unzip -q /opt/mcr_install/MATLAB_Runtime_${MATLAB_VERSION}_Update_3_glnxa64.zip -d /opt/mcr_install \
 && /opt/mcr_install/install -destinationFolder /opt/mcr -agreeToLicense yes -mode silent \
 && rm -rf /opt/mcr_install /tmp/*

# Install SPM Standalone in /opt/spm12/ 
ENV SPM_VERSION 12
ENV SPM_REVISION r7771
ENV LD_LIBRARY_PATH /opt/mcr/${MCR_VERSION}/runtime/glnxa64:/opt/mcr/${MCR_VERSION}/bin/glnxa64:/opt/mcr/${MCR_VERSION}/sys/os/glnxa64:/opt/mcr/${MCR_VERSION}/sys/opengl/lib/glnxa64:/opt/mcr/${MCR_VERSION}/extern/bin/glnxa64
ENV MCR_INHIBIT_CTF_LOCK 1
ENV SPM_HTML_BROWSER 0
# Running SPM once with "function exit" tests the succesfull installation *and*
# extracts the ctf archive which is necessary if singularity is going to be
# used later on, because singularity containers are read-only.
# Also, set +x on the entrypoint for non-root container invocations
RUN wget --no-check-certificate --progress=bar:force -P /opt https://www.fil.ion.ucl.ac.uk/spm/download/restricted/bids/spm${SPM_VERSION}_${SPM_REVISION}_Linux_${MATLAB_VERSION}.zip \
 && unzip -q /opt/spm${SPM_VERSION}_${SPM_REVISION}_Linux_${MATLAB_VERSION}.zip -d /opt \
 && rm -f /opt/spm${SPM_VERSION}_${SPM_REVISION}_Linux_${MATLAB_VERSION}.zip \
 && /opt/spm${SPM_VERSION}/spm${SPM_VERSION} function exit \
 && chmod +x /opt/spm${SPM_VERSION}/spm${SPM_VERSION}

# Add ANTS
WORKDIR /src
RUN mkdir ants
WORKDIR ants
RUN git clone https://github.com/ANTsX/ANTs.git
RUN mkdir build install
WORKDIR build
RUN cmake \
    ../ANTs -DCMAKE_INSTALL_PREFIX=/src/ants/install
RUN make
WORKDIR ANTS-build
RUN make install 

# Add Nifty Seg
WORKDIR /src
RUN git clone https://github.com/KCL-BMEIS/NiftySeg.git niftyseg
RUN mkdir niftyseg_build 
RUN mkdir /niftyseg_atlas
WORKDIR niftyseg_build
RUN cmake ../niftyseg -DINSTALL_PRIORS="TRUE" -DINSTALL_NIFTYREG="TRUE" -DINSTALL_PRIORS_DIRECTORY="/niftyseg_atlas" 
RUN make 
RUN make install

# FSL 
RUN apt update && apt install -y wget python

#install fsl, but get rid of src 
RUN wget https://fsl.fmrib.ox.ac.uk/fsldownloads/fslinstaller.py && python fslinstaller.py -d /usr/local/fsl -V 6.0.4 && rm -rf /usr/local/fsl/src

ENV FSLDIR=/usr/local/fsl
ENV PATH=$PATH:$FSLDIR/bin
ENV LD_LIBRARY_PATH=$FSLDIR/lib
ENV FSLOUTPUTTYPE=NIFTI_GZ

#fsl needs numpy
RUN apt install -y vim jq python-numpy




WORKDIR /


