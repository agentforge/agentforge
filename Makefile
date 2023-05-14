# Build targets
SSH_PRIVATE_KEY=`cat ~/.ssh/id_rsa`

.PHONY: build

# This has issues currently TODO Fix SSH_PRIVATE_KEY
core:
	docker build --build-arg REPO_URL=git@github.com:fragro/agentforge.git  --build-arg SSH_PRIVATE_KEY="$(SSH_PRIVATE_KEY)" -t agentforge -f ./docker/agentforge.Dockerfile .

build:
	docker build -t agent -f ./docker/agent.Dockerfile .
	docker build -t llm -f ./docker/llm.Dockerfile .
	docker build -t speech -f ./docker/speech.Dockerfile .
	docker build -t wav2lip -f ./docker/wav2lip.Dockerfile .

web:
	docker build -t web -f ./docker/web.Dockerfile .

# Run targets
run:
	cd ./docker && docker-compose up -d
