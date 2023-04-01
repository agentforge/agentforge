# Build targets
SSH_PRIVATE_KEY=`cat ~/.ssh/id_rsa`

.PHONY: build

build:
	docker build --build-arg REPO_URL=git@github.com:fragro/agent_n.git  --build-arg SSH_PRIVATE_KEY="$(SSH_PRIVATE_KEY)" -t worker -f ./docker/worker.Dockerfile .
	docker build --build-arg REPO_URL=git@github.com:fragro/agent_n.git  --build-arg SSH_PRIVATE_KEY="$(SSH_PRIVATE_KEY)" -t llm -f ./docker/llm.Dockerfile .
	docker build --build-arg REPO_URL=git@github.com:fragro/agent_n.git  --build-arg SSH_PRIVATE_KEY="$(SSH_PRIVATE_KEY)" -t speech -f ./docker/speech.Dockerfile .
	docker build --build-arg REPO_URL=git@github.com:fragro/agent_n.git  --build-arg SSH_PRIVATE_KEY="$(SSH_PRIVATE_KEY)" -t wav2lip -f ./docker/wav2lip.Dockerfile .
	docker build --build-arg REPO_URL=git@github.com:fragro/agent_n.git  --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" -t web -f ./docker/web.Dockerfile .
	docker build -t web2 -f ./docker/web2.Dockerfile .

# Install targets
install:
	cd ./docker && docker-compose up -d
