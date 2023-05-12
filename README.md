# agent_forge

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
- [x] DeepLake Service/Long-Term Vector Storage Memory
- [ ] Sentiment Classification Model/Service
- [ ] Named-Entity Recognition Model/Service
- [ ] Summarizer Service
- [ ] [Implement Quantization Patch](https://github.com/oobabooga/text-generation-webui/blob/main/modules/models.py)
- [ ] Worker/Queue for Model Services
- [ ] Always-Online Agent w/ Executive Function Loop
- [ ] Fall/Emergency Sound Detection Model
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
- Install latest docker-compose (>= 1.29.2 required):

```
sudo curl -L "https://github.com/docker/compose/releases/download/v2.17.3/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

If you aren't on x86 Linux change the URL to match your arch from the list of releases on the docker-compose github.

## Build Docker Containers For Development

### Build the web image:

```
docker build -t web -f ./docker/web.Dockerfile .
```
Now run `cd docker && python exec.py web` to start the docker container. To run the web server run the command `npx next dev`.

### Build the model ensemble stack:

Note: You only need to run the ensemble stack if you are pointing services to external services, have thick GPUs, or accept absurdly slow CPU inference speeds.

```
cd agent_n
docker build --build-arg REPO_URL=git@github.com:fragro/agent_n.git  --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" -t agentforge -f ./docker/agentforge.Dockerfile .
docker build -t worker -f ./docker/worker.Dockerfile .
docker build -t llm -f ./docker/llm.Dockerfile .
docker build -t speech -f ./docker/speech.Dockerfile .
docker build -t wav2lip -f ./docker/wav2lip.Dockerfile .
```
## Run the Web Instance Only (If Model Ensemble is Remote)

`docker-compose up -d web`

Connect to your Docker container, we provide a scrip to easily connect int the `/docker` folder. (python >= 3.8)

`python3 exec.py web`

Otherwise connect via `docker exec -it <CONTAINER_ID> /bin/bash`

To run the react typescript server:

```PORT=3000 npm start```

Change config.ts to point to the model ensemble IP.

## Run Entire Stack

Run all the services via docker-compose in the docker folder:

```docker-compose up -d```

## Running Model Ensemble APIs

To run the flask server(s) from inside a container:

```CONFIG_DIR="/app/agent_n/agentforge/config/configs/" flask run --host=0.0.0.0 --port=3000```

Wav2Lip (requires additional env vars):

```LC_ALL=C.UTF-8 LANG=C.UTF-8 CONFIG_DIR="/app/agent_n/agentforge/config/configs/" flask run --host=0.0.0.0 --port=3000```

## SSL

Create an ssl key and cert for the Flask API:

```openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365```

## Data Engine

Uses SQL Alchemy and Redis to store user credentials, profile, and training data.

To add new columns:

```flask db migrate -m "Migration message"```

## DeepLake

Coming Soon!
