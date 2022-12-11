# Use the huggingface/transformers-pytorch-deepspeed-latest-gpu-push-ci image as the base image
FROM huggingface/transformers-pytorch-deepspeed-latest-gpu-push-ci

ARG REPO_URL
ARG SSH_PRIVATE_KEY

ENV REPO_URL=$REPO_URL
ENV SSH_PRIVATE_KEY=$SSH_PRIVATE_KEY

RUN pip install gTTS flask pytest
RUN apt-get update && apt-get install -y git openssh-client

# Copy the cacher file to the container
COPY cache.py /app/

# Set the working directory to /app
WORKDIR /app

# Bust that cache
RUN python cache.py

# Copy over remaining libs
RUN mkdir -p /root/.ssh && \
    echo "$SSH_PRIVATE_KEY" > /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa

RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

RUN git clone "$REPO_URL"

# COPY app.py /app/
# COPY speech /app/speech
# COPY inference /app/inference

# Expose port 3000
EXPOSE 3000

# Run the Flask API
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]