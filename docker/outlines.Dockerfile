FROM nvidia/cuda:12.1.0-base-ubuntu22.04 AS vllm-base

# libnccl required for ray
RUN apt-get update -y \
    && apt-get install -y python3-pip


WORKDIR /workspace
COPY docker/requirements.txt requirements.txt
RUN apt install git -y
RUN pip install -r requirements.txt
    
ENV RESOURCE=LLM
RUN apt install cuda-toolkit-12-3 -y

WORKDIR /app
RUN pip install outlines[serve]  # install outlines and dependencies
RUN apt-get update -y && \
    apt-get install -y build-essential \
                       cmake \
                       git \
                       python3-dev \
                       libssl-dev \
                       libffi-dev \
                       libxml2-dev \
                       libxslt1-dev \
                       zlib1g-dev \
                       libncurses5-dev \
                       libgdbm-dev \
                       libnss3-dev \
                       libreadline-dev \
                       libsqlite3-dev \
                       libbz2-dev \
                       liblzma-dev \
                       curl \
                       wget \
                       unzip \
                       autoconf \
                       automake \
                       libtool \
                       pkg-config
# RUN pip install git+https://github.com/vllm-project/vllm

# install fix, don't install vllm dependency as it's pinned to vllm=0.2.8 on this branch, which isn't released yet
# RUN pip install git+https://github.com/lapp0/outlines@fix-vllm-new-tokenizer --no-deps
RUN pip install vllm==0.2.5 outlines==0.0.21
RUN pip install "pydantic>=2.0"
EXPOSE 8000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
