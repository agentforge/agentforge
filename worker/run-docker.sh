#/bin/bash
nvidia-docker run --ipc=host -it huggingface/transformers-pytorch-deepspeed-latest-gpu-push-ci /bin/bash