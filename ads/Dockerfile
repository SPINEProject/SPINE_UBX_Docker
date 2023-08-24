# Use the official Ubuntu base image
FROM ubuntu:jammy

# Set the working directory
WORKDIR /app

ENV DEBIAN_FRONTEND=nonintercative

# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y git curl make build-essential libhdf5-dev libssl-dev libfreetype6-dev liblcms2-dev libxcb1-dev libfribidi-dev libharfbuzz-dev libwebp-dev tcl8.6-dev python3-tk tk8.6-dev libjpeg8-dev libopenjp2-7-dev libtiff5-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py38_23.5.2-0-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

# Add Anaconda to PATH
ENV PATH /opt/conda/bin:$PATH

# cOPY FOLDER manually Downloaded from NITRC
COPY ADSv1.2 /app/ADSv1.2

# Set the working directory to the downloaded folder
WORKDIR /app/ADSv1.2

RUN conda create -p /app/ADSv1.2/ADS_ENV python=3.7.7 -y
#RUN . activate /app/ADSv1.2/ADS_ENV
RUN echo "source activate /app/ADSv1.2/ADS_ENV" > ~/.bashrc

ENV PATH="/app/ADSv1.2/ADS_ENV/bin:$PATH"

# # Verify pyenv setup
RUN python --version


# # Install Python dependencies
# ## RUN pip install --no-cache-dir -r codes/module_list.txt
# Install Python dependencies
RUN pip install numpy nibabel scipy scikit-image scikit-learn
RUN pip install h5py==2.10.0
RUN pip install dipy==1.4.0
RUN pip install tensorflow==2.0.0 
RUN pip install fury==0.7.0
RUN pip install pandas shap ipython
# ads repo mentions tensorflow 2.0.0 but might not be compatible with python version installed
RUN pip install --upgrade tensorflow

#   #might be used :  pip install tensorflow-gpu==2.0.0 \

# # add ADS python scripts to path
ENV PATH="/app/ADSv1.2/codes:$PATH"
