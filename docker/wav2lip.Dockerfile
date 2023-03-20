# 1. install a version of docker with gpu support (docker-ce >= 19.03)

# 2.  enter the project directory and build the wav2lip image:
# docker build -t wav2lip .

# 3. allow root user to connect to the display
# xhost +local:root

# 4. instantiate the container
# docker run --rm --gpus all -v /tmp/.X11-unix:/tmp/.X11-unix -v $PWD:/workspace/src -e DISPLAY=$DISPLAY --device /dev/dri -ti wav2lip bash

# NOTES:
# export CUDA_VISIBLE_DEVICES="" ## force cpu only

# Based on https://github.com/1adrianb/face-alignment/blob/master/Dockerfile

FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04

RUN export DEBIAN_FRONTEND=noninteractive RUNLEVEL=1 ; \
     apt-get update && apt-get install -y --no-install-recommends \
          build-essential cmake git curl ca-certificates \
          vim \
          python3-pip python3-dev python3-wheel \
          libglib2.0-0 libxrender1 python3-soundfile \
          ffmpeg && \
	rm -rf /var/lib/apt/lists/* && \
     pip3 install --upgrade setuptools

# RUN curl -o ~/miniconda.sh -O  https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
#      chmod +x ~/miniconda.sh && \
#      ~/miniconda.sh -b -p /opt/conda && \
#      rm ~/miniconda.sh

# ENV PATH /opt/conda/bin:$PATH

# RUN conda config --set always_yes yes --set changeps1 no && conda update -q conda
# RUN conda install pytorch torchvision cudatoolkit=10.1 -c pytorch

# # Install Wav2Lip package
# # NOTE we use the git clone to install the requirements only once
# # (if we use COPY it will invalidate the cache and  reinstall the dependencies for every change in the sources)
WORKDIR /workspace
RUN chmod -R a+w /workspace
RUN git clone https://github.com/Rudrabha/Wav2Lip
WORKDIR /workspace/Wav2Lip
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN mkdir -p /root/.cache/torch/checkpoints && \
     curl -SL -o /root/.cache/torch/checkpoints/s3fd-619a316812.pth "https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth"

# !!! NOTE !!! nvidia-driver version must match the version installed on the host(/docker server)
RUN export DEBIAN_FRONTEND=noninteractive RUNLEVEL=1 ; \
	apt-get update && apt-get install -y --no-install-recommends \
          nvidia-driver-450 mesa-utils && \
	rm -rf /var/lib/apt/lists/*

# create the working directory, to be mounted with the bind option
RUN mkdir /workspace/src
WORKDIR /workspace/src
