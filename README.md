<a href="https://agentforge.ai/">
  <div align="center">
  <img alt="AgentForge Backend and API" src="https://avatars.githubusercontent.com/u/135940999?s=96&v=4">
  </div>
  <h1 align="center">AgentForge</h1>
</a>

<p align="center">
  Where the Copilots of the Future are Forged
</p>

<p align="center">
  <a href="#the-cognitive-stack"><strong>The Cognitive Stack</strong></a> ·
  <a href="#the-agent"><strong>The Agent</strong></a> ·
  <a href="#infrastructure"><strong>Infrastructure</strong></a> ·
  <a href="#features"><strong>Features</strong></a> ·
  <a href="#installation"><strong>Installation</strong></a>
</p>
<br/>

## TLDR; The Cognitive Stack

- AgentForge is a modular framework and API to develop and deploy agents
- Agents observe, maintain beliefs, reason, communicate, and plan
- Agents are represented as a Directed Acyclic Graph (DAG) that combines composable subroutines into routines
- Subroutines are generic units of cognition and can intake data, run inference, employ classic AI algorithms, and much more
- Subroutines share a global Context, a form of working memory
- The Context also provides access to short-term and long-term memory, and other shared data
- Subroutines access lower level resources such as LLMs, Vision models, TTS through the Interface Factory

## The Agent

### Hierarchy of Thought

To simplify the development of agents we break the processes of agency down into composable subroutines.

The agent can be decomposed such that `Agent x -> Routine(x) -> [SubroutineA(x), SubroutineB(x) ...]` where `x` is the global Context.

At this time Agents are simple wrappers over a single routine but in the future will be extended to decide what routine needs to be run based on inputs.

Routines are a DAG of subroutines as described. All subroutines run until complete and results are either returned to the user or fed into the next iteration.

Subroutines usually access a single machine learning model or represent a single process to reduce complexity.

All subroutines fall into one of the following categories.
### Cognitive Categories

Our Agent design is aligned with the commonly implemented design for multi-agent systems.

1. Observation
1. Beliefs
1. Reasoning
1. Planning
1. Communication

### Observation
These subroutines are responsible for aggregating data from external sources, preprocessing as needed, and placing it into the shared Context.

### Beliefs

- Task Progress
- Agent State
- User and External Agent State
- Environmental State
- Source Knowledge
- Context

Beliefs include information about task progress, our agent's state, other agents or user's states, and the environment or scene's state. These are updated either through interaction with the agent or some form of offline/online learning.

Beliefs about user and agent state are stored in a symbolic predicate triplet, such as "Bob wants to grow tomatoes". This yields `<Bob, wants to grow, tomatoes>`. This can then be stored in the open query predicate language (OQPL).

Task state and message history are stored in the database. Source Knowledge is stored in a vectorstore for Retrieval augmented generation. Context is stored in locally for a single Routine iteration and then is discarded.

### Reasoning
Reasoning subroutines take the current state, a list of all available actions, and determines a high-level course of action. Since the environment is partially observable the agent needs to query the environment or user as part of its reasoning process.

To accomplish this we use a few-shot CoT approach.

- Identify Task Domain via Intent Subroutine
- Identify knowledge needed for domain 
- Loop through queries for missing data from observations or by communication with user about their goals, necessary objects and pre-conditions.
- For each query if response is natural language use few-shot CoT for data-type to translate to symbolic graph. This is a closed set of few-shot examples because we can constrain the results to a set of types, string, boolean, numeric, etc.

This process allows the agent to reason in a defined PDDL domain however these domains must be curated.
### Planning

Transforms higher-level reasoning and knowledge into a low-level instruction format.

- Once all gaps in knowledge have been satisfied create a PDDL problem valid for this domain
- Use FastDownward to identify low-level instructions that satisfy the desired goal(s)
- Translate to NLP and create user Task or create Agent Task and implement the low-level instructions

### Communication

LLM response to the user based on the context added to the prompt by the previous modules.

## Infrastructure

The interface_factory provides generic access to interfaces such as APIs, models, and algorithms. Each interface is generically defined through an Adapter of its type, i.e. the Database adapter

Each service is deployed as a docker container which share a docker Volume or other file-system. The specific services and API details we use are defined by environment variables and accessed via the factory function.

To create a new interface you must:

- Create an adapter or select an existing one
- Implement the adapter pattern for your specific service
- Add logic to the interface_factory to expose your new service

## Features

### High-Level Features

- [x] Few-Shot CoT Reasoning
- [x] PDDL Fast-Downward Planning
- [x] Long-Term Memory Vectorstore
- [x] Short-Term Memory Session History
- [x] Large Language Model
- [x] Text To Speech
- [x] Lipsync Speech to Video (NC)
- [x] Semantic Intent Detection
- [x] Open Query Predicate Language
- [x] Predicate Extraction
- [x] Audio/Video Streaming
- [ ] Vision Captioning and Q/A Model
- [ ] Sentiment Analysis Model
- [ ] Summarization Model
- [ ] Direct Policy Optimization
- [ ] PDDL Planning Artifact Generator

### Models, Embeddings, and Algorithms

- [x] HF Transformers
- [x] ctransformers
- [x] Coqai TTS
- [x] Wav2Lip
- [x] SadTalker
- [x] BarkTTS
- [x] PDDL Fast Downward
- [x] Deeplake Vectorstore
- [x] Milvus Vectorstore
- [ ] Conversational [Whisper](https://github.com/sanchit-gandhi/whisper-jax)

## Installation

### Requirements

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

### Build the web image:

Clone the agentforge-client, copy and fill out the the `.env.example` or get a development `.env` from the team.

```
docker build -t client -f ./Dockerfile .
```

After building the image run the client:

`docker-compose up -d client`

Connect via `docker exec -it agentforge-client_client_1 /bin/bash`

To run the react typescript server:

```npx next dev -p 8090```

### Build the model ensemble stack

Note: You only need to run the ensemble stack if you are pointing services to external services, have thick GPUs, or accept absurdly slow CPU inference speeds.

First copy over your development `.env` file or copy the `.env.example`

```
cd agentforge
make build
make run
```

### Run Entire Stack

Run all the services via docker-compose in the docker folder:

```docker-compose up -d```

### Running Model Ensemble APIs

To run the FastAPI server(s) from inside the container:

> Note: For development containers you will need to run the following processes for a full stack.

On the Agent container:
```
API_DOMAIN="https://mite-inspired-snipe.ngrok-free.app" WEBSITE_DOMAIN="https://greensage.app" PYTHONPATH="/app/agentforge/" uvicorn main:app --reload --host=0.0.0.0 --port=3000
```

Dev:
```
API_DOMAIN="https://api.agentforge.ai.ngrok-free.app" WEBSITE_DOMAIN="https://agentforge.ngrok.dev" PYTHONPATH="/app/agentforge/" uvicorn main:app --reload --host=0.0.0.0 --port=3005
```

On the LLM container:
```
PYTHONPATH="/app/agentforge/" uvicorn llm:app --reload --host=0.0.0.0 --port=3000
```

On the Speech container:
```
PYTHONPATH="/app/agentforge/" uvicorn tts:app --reload --host=0.0.0.0 --port=3000
```

On the Wav2Lip container:
```
PYTHONPATH="/app/agentforge/" uvicorn w2l:app --reload --host=0.0.0.0 --port=3000
```

On the VQA container:
```
PYTHONPATH="/app/agentforge/" uvicorn vqa:app --reload --host=0.0.0.0 --port=3000
```

On the PixArt container:
```
PYTHONPATH="/app/agentforge/" uvicorn pixart:app --reload --host=0.0.0.0 --port=8000
```

On the tokenizer container:
```
PYTHONPATH="/app/agentforge/" uvicorn tokenizer:app --reload --host=0.0.0.0 --port=3000
```

VLLM
```
python -m vllm.entrypoints.api_server \
--model TheBloke/Speechless-Llama2-Hermes-Orca-Platypus-WizardLM-13B-AWQ \
--quantization awq \
--max-num-batched-tokens 4096
```

Outlines

```
python3 -m outlines.serve.serve --model NousResearch/Meta-Llama-3-8B-Instruct --max-num-batched-tokens 8192
```

```
python3 -m outlines.serve.serve --model TheBloke/Speechless-Llama2-Hermes-Orca-Platypus-WizardLM-13B-AWQ --quantization awq --max-num-batched-tokens 4096
```

```
python3 -m outlines.serve.serve --model PrunaAI/Meta-Llama-3-8b-instruct-AWQ-smashed --quantization awq --max-num-batched-tokens 8192
```

### Generating a Universe From Scratch

For Final Frontier

#### Generate a Galaxy + Planets:
```
from agentforge.api.sim import get_galaxy
galaxy = await get_galaxy("milky_way4275", num_systems=2000, anim_steps=10)
```

#### Evolve Life:
First run workers:
```
celery -A agentforge.api.sim worker --loglevel=INFO -n worker1@%h
celery -A agentforge.api.sim worker --loglevel=INFO -n worker2@%h
celery -A agentforge.api.sim worker --loglevel=INFO -n worker3@%h
celery -A agentforge.api.sim worker --loglevel=INFO -n worker4@%h
```

Next run evolve:
```
from agentforge.api.sim import evolve_life
evolve_life.delay()

```