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

# elder-link API
RUN git clone "$REPO_URL"

# Stable Diffusion - Fun Times
RUN git clone git@github.com:CompVis/stable-diffusion.git
RUN git clone git@github.com:jquesnelle/txt2imghd.git

RUN pip install gTTS flask pytest accelerate bitsandbytes trl pip install flair flask_cors
RUN pip install --upgrade diffusers[torch]
RUN apt-get update && apt-get install -y git openssh-client

RUN . /root/.bashrc && \
    conda init bash && \
    conda env create -f stable-diffusion/environment.yaml && \
    conda update -n base conda

# RUN conda init bash
# RUN conda env create -f stable-diffusion/environment.yaml
# RUN source ~/.bashrc && conda activate ldm

RUN wget -P /app/cache/ https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt

RUN mkdir -p /root/stable-diffusion/models/ldm/stable-diffusion-v1
RUN ln -s /app/cache/v1-5-pruned-emaonly.ckpt /root/stable-diffusion/models/ldm/stable-diffusion-v1/model.ckpt 

# Bust that cache
# RUN python cache.py

# COPY app.py /app/
# COPY speech /app/speech
# COPY inference /app/inference

# FIX FOR packaging.version.InvalidVersion: Invalid version: '0.10.1,<0.11'
# Run twice to grab all version
RUN pip uninstall -y packaging transformers torchmetrics
RUN pip uninstall -y packaging transformers torchmetrics
# Reinstall with specific versions
RUN pip install transformers==4.26.1
RUN pip install packaging==21.3
RUN pip install 'torchmetrics<0.8'


# Expose port 3000
EXPOSE 3000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
