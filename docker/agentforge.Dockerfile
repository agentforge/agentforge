# Use the huggingface/transformers-pytorch-deepspeed-latest-gpu-push-ci image as the base image
FROM huggingface/transformers-pytorch-deepspeed-latest-gpu-push-ci

# Set the working directory to /app
RUN mkdir -p /app/agent_n
COPY . /app/agent_n/

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get install -y libstdc++6-7-dbg ffmpeg git openssh-client tig

# RUN rm /usr/lib/x86_64-linux-gnu/libstdc++.so.6 && ln -s /opt/conda/x86_64-conda-linux-gnu/lib/libstdc++.so.6.0.30 /usr/lib/x86_64-linux-gnu/libstdc++.so.6

RUN pip install --upgrade pip

WORKDIR /app/agent_n/agentforge/
RUN mkdir /app/agent_n/logs/
RUN pip install -r /app/agent_n/agentforge/requirements.txt

# #CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
