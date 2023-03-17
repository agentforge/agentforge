# Build targets
SSH_PRIVATE_KEY=`cat ~/.ssh/id_rsa`

.PHONY: build

build:
	docker build --build-arg REPO_URL=git@github.com:fragro/agent_n.git  --build-arg SSH_PRIVATE_KEY="$(SSH_PRIVATE_KEY)" -t worker -f ./docker/worker.Dockerfile .
	docker build --build-arg REPO_URL=git@github.com:fragro/agent_n.git  --build-arg SSH_PRIVATE_KEY="$(SSH_PRIVATE_KEY)" -t llm -f ./docker/llm.Dockerfile .

# Install targets
install:
	cd ./docker && docker-compose up -d
