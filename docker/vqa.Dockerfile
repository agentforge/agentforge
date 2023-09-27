FROM huggingface/transformers-pytorch-deepspeed-latest-gpu-push-ci
ENV RESOURCE=VQA

# Set the working directory to /app
RUN mkdir -p /app/agentforge
COPY . /app/agentforge/
ENV PYTHONPATH "${PYTHONPATH}:/app/agentforge"

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get install -y libstdc++6-7-dbg ffmpeg git openssh-client tig

# RUN rm /usr/lib/x86_64-linux-gnu/libstdc++.so.6 && ln -s /opt/conda/x86_64-conda-linux-gnu/lib/libstdc++.so.6.0.30 /usr/lib/x86_64-linux-gnu/libstdc++.so.6

RUN pip install --upgrade pip

WORKDIR /app/agentforge/agentforge/
RUN mkdir /app/agentforge/logs/
RUN pip install -r /app/agentforge/requirements.txt
COPY .env /app/agentforge/.env

WORKDIR /
#RUN git lfs install
RUN git clone https://huggingface.co/bibimbap/Qwen-VL-Chat-Int4
WORKDIR Qwen-VL-Chat-Int4
# Install the dependencies from requirements.txt
RUN pip install -r requirements.txt
WORKDIR /app/agentforge/agentforge/api

RUN pip install optimum
RUN pip install auto-gptq
RUN pip install peft einops
RUN pip install 'accelerate @ git+https://github.com/huggingface/accelerate.git'
RUN pip install flash-attn==1.0.3.post0
RUN pip install triton==2.0.0.dev20221202
RUN pip install torch==1.13.1
RUN pip install xformers
RUN CT_CUBLAS=1 pip install ctransformers --no-binary ctransformers
# Expose port 3000

EXPOSE 3000

# RUN git clone https://github.com/JustinLin610/AutoGPTQ.git 
# WORKDIR AutoGPTQ
# RUN pip install -v .

# WORKDIR /

# EXPOSE 3000
CMD tail -f /dev/null