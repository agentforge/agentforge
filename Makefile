# Build targets
SSH_PRIVATE_KEY=`cat ~/.ssh/id_rsa`

.PHONY: build

# This has issues currently TODO Fix SSH_PRIVATE_KEY
core:
	docker build --build-arg REPO_URL=git@github.com:fragro/agent_n.git  --build-arg SSH_PRIVATE_KEY="$(SSH_PRIVATE_KEY)" -t historica -f ./docker/worker.Dockerfile .

build:
	docker build -t worker -f ./docker/worker.Dockerfile .
	docker build -t llm -f ./docker/llm.Dockerfile .
	docker build -t speech -f ./docker/speech.Dockerfile .
	docker build -t wav2lip -f ./docker/wav2lip.Dockerfile .
	docker build -t web2 -f ./docker/web2.Dockerfile .

# Run targets
run:
	cd ./docker && docker-compose up -d
