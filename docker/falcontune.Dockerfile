# Use NVIDIA's official CUDA 11.8 base image
FROM nvidia/cuda:11.8.0-devel-ubuntu20.04

# Maintained by AgentForge
LABEL maintainer="info@agentforge.ai"

# Set environment variables to avoid tzdata interactive configuration
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git python3 python3-pip python3-dev && \
    ln -s /usr/bin/python3 /usr/bin/python

# Set CUDA_HOME environment variable
ENV CUDA_HOME /usr/local/cuda

# Clone the repository
RUN git clone https://github.com/rmihaylov/falcontune.git

# Set working directory
WORKDIR falcontune

# Install the dependencies from requirements.txt
RUN pip install -r requirements.txt

# Install falcontune
RUN python setup.py install

# Install falcontune with CUDA support
RUN python setup_cuda.py install

# Command to keep container running
CMD ["tail", "-f", "/dev/null"]
