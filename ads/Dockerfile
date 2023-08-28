# Use the official Ubuntu base image
FROM ubuntu:jammy

# Set the working directory
WORKDIR /app

ENV DEBIAN_FRONTEND=nonintercative

# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y git curl make build-essential libhdf5-dev libssl-dev libfreetype6-dev liblcms2-dev libxcb1-dev libfribidi-dev libharfbuzz-dev libwebp-dev tcl8.6-dev python3-tk tk8.6-dev libjpeg8-dev libopenjp2-7-dev libtiff5-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev

# install locales
RUN apt-get install -y \
        locales 

RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8   

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py38_23.5.2-0-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

# Add Anaconda to PATH
ENV PATH /opt/conda/bin:$PATH

# cOPY FOLDER manually Downloaded from NITRC
COPY ADSv1.2 /app/ADSv1.2
COPY isHD5Valid.py /app/ADSv1.2/codes/
COPY loadModel.py /app/ADSv1.2/codes/

# Set the working directory to the downloaded folder
WORKDIR /app/ADSv1.2

RUN conda create -p /app/ADSv1.2/ADS_ENV python=3.6.5 -y
#RUN . activate /app/ADSv1.2/ADS_ENV
RUN echo "source activate /app/ADSv1.2/ADS_ENV" > ~/.bashrc

ENV PATH="/app/ADSv1.2/ADS_ENV/bin:$PATH"

# # Verify pyenv setup
RUN python --version


# # Install Python dependencies
# ## RUN pip install --no-cache-dir -r codes/module_list.txt
# Install Python dependencies
RUN pip install numpy==1.19.5 nibabel==3.2.1 scipy==1.4.1 scikit-image scikit-learn==0.24.1
RUN pip install pandas shap ipython
RUN pip install h5py==2.10.0
RUN pip install dipy==1.4.0
RUN pip install tensorflow==2.0.0  
RUN pip install fury==0.7.0
RUN pip install xlrd==1.2.0
#2.6.2
# ads repo mentions tensorflow 2.0.0 but might not be compatible with python version installed
#RUN pip install --upgrade tensorflow

#   #might be used :  pip install tensorflow-gpu==2.0.0 \

## Prepare testing dataset to test ADS
RUN mkdir /mypath && \
    mkdir /mypath/subject_directory  &&  \
    echo "/app/ADSv1.2/data/examples/Subject01" > /mypath/subject_directory/subject_directory_path_list.txt 

# # add ADS python scripts to path
ENV PATH="/app/ADSv1.2/codes:$PATH"
