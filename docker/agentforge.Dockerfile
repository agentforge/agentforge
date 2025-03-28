# Use the huggingface/transformers-pytorch-deepspeed-latest-gpu-push-ci image as the base image
FROM huggingface/transformers-pytorch-deepspeed-latest-gpu-push-ci

# Set the working directory to /app
RUN mkdir -p /app/agentforge
ENV PYTHONPATH "${PYTHONPATH}:/app/agentforge"

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get install -y libstdc++6-7-dbg ffmpeg git openssh-client tig

# RUN rm /usr/lib/x86_64-linux-gnu/libstdc++.so.6 && ln -s /opt/conda/x86_64-conda-linux-gnu/lib/libstdc++.so.6.0.30 /usr/lib/x86_64-linux-gnu/libstdc++.so.6

RUN apt install -y python3.9
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
RUN update-alternatives --config python3
RUN wget https://bootstrap.pypa.io/get-pip.py && python3 ./get-pip.py
RUN pip install --upgrade pip
RUN pip install Cython
RUN apt-get install -y libpython3.9-dev

COPY . /app/agentforge/
WORKDIR /app/agentforge/agentforge/
RUN mkdir /app/agentforge/logs/
RUN pip install -r /app/agentforge/requirements.txt
COPY .env /app/agentforge/.env

# #CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
