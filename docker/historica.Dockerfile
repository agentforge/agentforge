# Use the huggingface/transformers-pytorch-deepspeed-latest-gpu-push-ci image as the base image
FROM huggingface/transformers-pytorch-deepspeed-latest-gpu-push-ci

ARG REPO_URL
ARG SSH_PRIVATE_KEY

ENV REPO_URL=$REPO_URL
ENV SSH_PRIVATE_KEY=$SSH_PRIVATE_KEY

# Set the working directory to /app
WORKDIR /app

# Copy over git repos
RUN mkdir -p /root/.ssh && \
    echo "$SSH_PRIVATE_KEY" > /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa

RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

# agent_n API
RUN git clone "$REPO_URL"

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get install -y libstdc++6-7-dbg ffmpeg git openssh-client tig

# RUN rm /usr/lib/x86_64-linux-gnu/libstdc++.so.6 && ln -s /opt/conda/x86_64-conda-linux-gnu/lib/libstdc++.so.6.0.30 /usr/lib/x86_64-linux-gnu/libstdc++.so.6

RUN pip install --upgrade pip
RUN pip install llvmlite --ignore-installed

WORKDIR /app/agent_n/historica/
RUN pip install -r /app/agent_n/historica/requirements.txt

# #CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
