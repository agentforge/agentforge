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
- [ ] Worker/Queue for Model Services
- [ ] Always-Online Agent w/ Executive Function Loop
- [ ] Caretake Executive Function Example
- [ ] Avatar Creator on Web
- [ ] Make Services and Models Configurable through Web Interface/DB
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

- [Install Docker or Docker Engine for Linux](https://docs.docker.com/get-docker/)
- CUDA capable Nvidia GPU + Drivers (if running GPU services locally)
- Install docker-compose >= 1.29.2:

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

## Build Docker Containers

Build the web image:

```
docker build --build-arg REPO_URL=git@github.com:fragro/agent_n.git  --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" -t web2 -f ./docker/web2.Dockerfile .
```

Note: You only need to run the ensemble stack if you are pointing services to external services, have thick GPUs, or accept absurdly slow CPU inference speeds.


Build the model ensemble stack:

```
cd agent_n
docker build --build-arg REPO_URL=git@github.com:fragro/agent_n.git  --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" -t historica -f ./docker/historica.Dockerfile .
docker build -t worker -f ./docker/worker.Dockerfile .
docker build -t llm -f ./docker/llm.Dockerfile .
docker build -t speech -f ./docker/speech.Dockerfile .
docker build -t wav2lip -f ./docker/wav2lip.Dockerfile .
```
## Run the Web Instance Only (If Model Ensemble is Remote)

`docker-compose up -d web`

Change config.ts to point to the model ensemble IP.

## Run Entire Stack

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
