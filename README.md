# agent_n

Playground for integrating agents with deeplearning micro-services.

## Features
- [x] Flask proxy
- [x] Basic Conversational Memory
- [x] JSON Configurable Avatar System
- [x] Wav2Lip generated video
- [x] coqai TTS.py generated audio
- [x] PromptManager
- [x] Llama/Alpaca
- [x] HuggingFace
- [x] Streaming
- [x] SSE Events for Streaming
- [x] React/Typescript Frontend
- [x] Multi-GPU Inference
- [x] whisper/large (buggy currently)
- [x] Rails Prototype (deprecated)
- [ ] DeepLake Service/Long-Term Vector Storage Memory
- [ ] Always-Online Agent w/ Executive Function Loop
- [ ] Caretake Executive Function Example
- [ ] Avatar Creator
- [ ] Avatar Library (Share, Remix, Report Avatars)
- [ ] [whisper/fast](https://github.com/sanchit-gandhi/whisper-jax)
- [ ] PRISMR Object Detection
- [ ] Convert Flask to Fast API
- [ ] Audio Data Aggregation Pipeline
- [ ] [Winfredy / SadTalker](https://github.com/Winfredy/SadTalker)
- [ ] [Bark TTS](https://github.com/suno-ai/bark)
- [ ] Integrate Latest Langchain
- [ ] LORA Fine-Tuning w/ External Library
- [ ] [PPO With TRL](https://github.com/lvwerra/trl)
- [ ] Fine-Tuning or PPO w/ Long-Term Vector Memory Storage
- [ ] Mobile Application

## Requirements

Minimalistic requirements:

- [Install Docker](https://docs.docker.com/get-docker/)
- CUDA capable Nvidia GPU + Drivers (if running GPU services locally)

## Run the Web Instance

`docker-compose up -d web`

Change config.ts to point to the model ensemble IP.

## Build for Dev

Install docker-compose >= 1.29.2:

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

Build the primary Docker image:

```docker build --build-arg REPO_URL=git@github.com:fragro/agent_n.git  --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" -t historica -f ./docker/historica.Dockerfile .```

Now build the rest of the containers:

```make build```

## Run

Run all the services via docker-compose in the docker folder:

```docker-compose up -d```

## SSL

Create an ssl key and cert for the Flask API:

```openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365```

## Development

To run the flask server(s) from inside a container:

```CONFIG_DIR="/app/agent_n/historica/config/configs/" flask run --host=0.0.0.0 --port=3000```

Wav2Lip (requires additional env vars):

```LC_ALL=C.UTF-8 LANG=C.UTF-8 CONFIG_DIR="/app/agent_n/historica/config/configs/" flask run --host=0.0.0.0 --port=3000```

To run the react typescript server:

```PORT=3005 npm start```

## Data Engine

Uses SQL Alchemy and Redis to store user credentials, profile, and training data.

To add new columns:

```flask db migrate -m "Migration message"```

## DeepLake

Coming Soon!
