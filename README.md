# agent_n

To build the Docker image, run the following command:

```docker build --build-arg REPO_URL=git@github.com:fragro/elder-link.git  --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" -t worker .```

To run the Docker container, run the following command:

```nvidia-docker run --ipc=host -p 3000:3000 worker .```

To run an interactive shell use this instead:

```nvidia-docker run -it --ipc=host -p 3000:3000 worker /bin/bash```

To run the flask server:

```CONFIG_DIR="/app/agent_n/core/config/configs/" flask run --host=0.0.0.0 --port=3000```

To run the rails server:

```rails server -p 3001```

Running redis:

```docker run --name agent-redis -d redis redis-server --save 60 1 --loglevel warning```
