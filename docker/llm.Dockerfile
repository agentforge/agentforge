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

RUN pip install gTTS flask pytest accelerate bitsandbytes trl pip install flask_cors fuzzywuzzy fuzzysearch python-Levenshtein
RUN pip install --upgrade diffusers[torch]
RUN apt-get update && apt-get install -y git openssh-client
RUN pip install 'langchain @ git+https://github.com/fragro/langchain.git'
RUN pip uninstall -y packaging transformers torchmetrics

# Reinstall with specific versions
# RUN pip install transformers==4.26.1
RUN pip install 'git+https://github.com/huggingface/transformers.git'
RUN pip install packaging==21.3
RUN pip install 'torchmetrics<0.8'
RUN pip install espnet
RUN pip install espnet_model_zoo
RUN conda install -c conda-forge gcc=12.1.0
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get update
RUN apt-get install -y libstdc++6-7-dbg
RUN pip install numpy==1.23.5
RUN apt-get install -y tig ffmpeg
RUN rm /usr/lib/x86_64-linux-gnu/libstdc++.so.6 && ln -s /opt/conda/x86_64-conda-linux-gnu/lib/libstdc++.so.6.0.30 /usr/lib/x86_64-linux-gnu/libstdc++.so.6
RUN pip install --upgrade pip
RUN pip install redis rq
RUN pip install pygments peft


# Expose port 3000
EXPOSE 3000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
