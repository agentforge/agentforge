# agent_n

Playground for integrating agents with deeplearning micro-services.

## Features

### Agent
- [x] RESTful Service proxy
- [x] Conversational Memory
- [ ] Multi-Agent Forum

### Agent Tools
- [x] Search
- [ ] REPL
- [ ] Task Plan Loop

### Avatars
- [x] Configurable Avatar System
- [ ] Avatar Creation Pipeline

### Speech To Animation
- [x] Wav2Lip
- [ ] Winfredy / SadTalker

### Speech Encoding
- [x] TTS.py
- [ ] Improve text-preprocessing
- [ ] Audio Data Aggregation/Cleanup
- [ ] LORA Fine-Tuning

### Language Model
- [x] Alpaca-LORA-7B w/ PEFT
- [x] Streaming
- [ ] OpenAI API Integration

#### Fine-Tuning
- [ ] LORA Fine-Tuning w/ Anarchist Library for Makhno Avatar 

#### RLHF (Reinforcement Learning through Human Feedback)
- [ ] Integrate RLHF

### Speech Decoding
- [ ] whisper/large

### Computer Vision
- [ ] PRISMR Object Detection

### Web Frontend
- [x] Rails Prototype
- [ ] SSE Events for Streaming
- [ ] React/Typescript Production Level App
- [ ] Mobile-First Approach

## Requirements

Minimalistic requirements.

- Docker
- CUDA capable nvidia GPU + drivers

## Build for Dev

Create an ssl key and cert for the Flask API:

```openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365```

Install docker-compose >= 1.29.2:

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

Build the primary Docker image:

```docker build --build-arg REPO_URL=git@github.com:fragro/agent_n.git  --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" -t historica -f ./docker/worker.Dockerfile .```

Now build the rest of the containers:

```make build```

## Run

Run all the services via docker-compose in the docker folder:

```docker-compose up -d```

TODO: Running in prod

## Development

To run the flask server(s) from inside a container:

```CONFIG_DIR="/app/agent_n/historica/config/configs/" flask run --host=0.0.0.0 --port=3000```

Wav2Lip (requires additional env vars):

```LC_ALL=C.UTF-8 LANG=C.UTF-8 CONFIG_DIR="/app/agent_n/historica/config/configs/" flask run --host=0.0.0.0 --port=3000```

To run the react typescript server:

```PORT=3005 npm start```

Running the rails server (deprecated):

```rails server -p 3001```

## Data Engine

Uses SQL Alchemy and Redis to store user credentials, profile, and training data.

To add new columns:

```flask db migrate -m "Migration message"```
