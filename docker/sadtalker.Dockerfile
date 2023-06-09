FROM huggingface/transformers-pytorch-deepspeed-latest-gpu-push-ci
ENV RESOURCE=W2L

# Set the working directory to /app
RUN mkdir -p /app/agentforge
COPY . /app/agentforge/

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get install -y libstdc++6-7-dbg ffmpeg git openssh-client tig

# RUN rm /usr/lib/x86_64-linux-gnu/libstdc++.so.6 && ln -s /opt/conda/x86_64-conda-linux-gnu/lib/libstdc++.so.6.0.30 /usr/lib/x86_64-linux-gnu/libstdc++.so.6

RUN pip install --upgrade pip

WORKDIR /app/agentforge/agentforge/
RUN mkdir /app/agentforge/logs/
COPY .env /app/agentforge/.env

RUN apt update && apt install -y libsm6 libxext6
RUN apt-get install -y libxrender-dev
RUN pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
RUN conda install ffmpeg
RUN pip install -r /app/agentforge/agentforge/interfaces/sadtalker/requirements.txt

#如需使用DAIN模型进行补帧需安装paddle
# CUDA 11.2
RUN python -m pip install paddlepaddle-gpu==2.3.2.post112 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html

RUN pip uninstall -y opencv-python && pip install opencv-python==4.7.0.72
RUN pip uninstall -y opencv-contrib-python && pip install opencv-contrib-python==4.7.0.72
RUN pip uninstall -y numpy && pip install numpy==1.23.5
RUN pip install "opencv-python-headless<4.3"

WORKDIR /app/agentforge/agentforge/api/wav2lip

# Expose port 3000
EXPOSE 3000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
