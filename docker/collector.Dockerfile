# Use Ubuntu as a base image
FROM ubuntu:latest

# Install Python 3.9 and other dependencies
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    git \
    wget

# Install pandoc
RUN wget https://github.com/jgm/pandoc/releases/download/2.14.2/pandoc-2.14.2-1-amd64.deb && \
    dpkg -i pandoc-2.14.2-1-amd64.deb && \
    rm pandoc-2.14.2-1-amd64.deb

# Set the working directory in the container
WORKDIR /app

# Clone the git repository
RUN git clone https://github.com/agentforge/anything-llm.git .

# Install virtualenv
RUN python3 -m pip install virtualenv

# Setup virtual environment and install dependencies
RUN python3 -m virtualenv v-env && \
    . v-env/bin/activate && \
    pip install -r collector/requirements.txt

# Copy example env file as .env
RUN cp collector/.env.example collector/.env

# Keep container alive
CMD tail -f /dev/null
