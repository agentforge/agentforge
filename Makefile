# Build targets
.PHONY: build

build:
	docker build -t agentforge -f ./docker/agentforge.Dockerfile .
	docker build -t agent -f ./docker/agent.Dockerfile .
	docker build -t llm -f ./docker/llm.Dockerfile .
	docker build -t speech -f ./docker/speech.Dockerfile .
	docker build -t wav2lip -f ./docker/wav2lip.Dockerfile .

web:
	docker build -t web -f ./docker/web.Dockerfile .

# Run targets
run:
	cd ./docker && docker-compose up -d
