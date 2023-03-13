# Build targets
build:
	docker build --build-arg REPO_URL=git@github.com:fragro/agent_n.git  --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" -t worker ./docker/worker.Dockerfile
	docker build --build-arg REPO_URL=git@github.com:fragro/agent_n.git  --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" -t llm ./docker/llm.Dockerfile

# Install targets
install:
	docker-compose up -d