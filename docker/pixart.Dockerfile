FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Set working directory
WORKDIR /workspace

# Install git and other dependencies
RUN apt-get update && \
    apt-get install -y \
        git \
        python3 \
        python-is-python3 \
        python3-pip \
        python3.10-venv \
        libgl1 \
        libgl1-mesa-glx \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Clone the PixArt-alpha repository
RUN git clone https://github.com/PixArt-alpha/PixArt-alpha.git /workspace/PixArt-alpha

# Change to the directory of the cloned repository
WORKDIR /workspace/PixArt-alpha

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of your code or additional files if needed
COPY . /app/agentforge/
WORKDIR /app/agentforge/agentforge/
RUN mkdir /app/agentforge/logs/
# RUN pip install -r /app/agentforge/requirements.txt
COPY .env /app/agentforge/.env

# Your other Dockerfile commands...
EXPOSE 8000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
