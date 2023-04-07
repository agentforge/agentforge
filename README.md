# agent_n

Playground for integrating agents with deeplearning micro-services.

## Requirements

Minimalistic requirements.

- Docker
- CUDA capable nvidia GPU + drivers

## Build

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
