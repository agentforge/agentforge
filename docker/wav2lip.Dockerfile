FROM agentforge:latest
ENV RESOURCE=W2L

RUN apt update && apt install -y libsm6 libxext6
RUN apt-get install -y libxrender-dev
RUN pip uninstall -y opencv-python && pip install opencv-python==4.7.0.72
RUN pip uninstall -y opencv-contrib-python && pip install opencv-contrib-python==4.7.0.72
RUN pip uninstall -y numpy && pip install numpy==1.23.5
RUN pip install "opencv-python-headless<4.3"

RUN mkdir -p /root/.cache/torch/checkpoints && \
     curl -SL -o /root/.cache/torch/checkpoints/s3fd-619a316812.pth "https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth"

# Clone wave2lip
RUN git clone https://github.com/Rudrabha/Wav2Lip.git

#RUN mkdir /app/agentforge/agentforge/wav2lip/temp

WORKDIR /app/agentforge/agentforge/api/wav2lip

# Expose port 3000
EXPOSE 3000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
