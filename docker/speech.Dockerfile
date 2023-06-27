# Use the huggingface/transformers-pytorch-deepspeed-latest-gpu-push-ci image as the base image
ARG BASE=nvidia/cuda:11.8.0-base-ubuntu22.04
FROM ${BASE}
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends gcc g++ make python3 python3-dev python3-pip python3-venv python3-wheel espeak-ng libsndfile1-dev && rm -rf /var/lib/apt/lists/*
RUN pip3 install llvmlite --ignore-installed

WORKDIR /root
COPY . /root
RUN pip3 install torch torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
RUN rm -rf /root/.cache/pip

# Set the working directory to /app
RUN mkdir -p /app/agentforge
COPY . /app/agentforge/

ENV RESOURCE=TTS

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get install -y ffmpeg git openssh-client tig

# RUN rm /usr/lib/x86_64-linux-gnu/libstdc++.so.6 && ln -s /opt/conda/x86_64-conda-linux-gnu/lib/libstdc++.so.6.0.30 /usr/lib/x86_64-linux-gnu/libstdc++.so.6

RUN pip install --upgrade pip

WORKDIR /app/agentforge/agentforge/
RUN mkdir /app/agentforge/logs/
# RUN pip install -r /app/agentforge/requirements.txt
COPY .env /app/agentforge/.env

# #CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null

# RUN apt-get install -y espeak-ng
# RUN pip install "typeguard==2.7.0"
# RUN pip install TTS inflect redis pymongo sentence_transformers --ignore-installed llvmlite
# # RUN pip install git+https://github.com/suno-ai/bark.git
# RUN pip uninstall -y psutil
# RUN pip uninstall -y urllib3 && pip install urllib3==1.26
# RUN pip install "scipy<1.9.0,>=1.7.0"
# RUN pip install --ignore-installed "numba==0.55.1"
# RUN pip install "soundfile>=0.12.1"
# RUN pip install "networkx<3.0.0,>=2.5.0"
# RUN pip install "pydantic!=1.8,!=1.8.1,<1.9.0,>=1.7.4"
# RUN pip install "click<8.1.0"
# RUN pip install "flask==2.2.2"
# RUN pip install "langchain==0.0.133"
# RUN pip install "pydantic==1.10.8"
# RUN pip install sentence_transformers
# RUN python -m pip install python-dotenv
WORKDIR /app/agentforge/agentforge/api

# Expose port 3000
EXPOSE 3000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
