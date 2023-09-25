FROM agentforge:latest
ENV RESOURCE=VQA

#RUN git lfs install
RUN git clone https://huggingface.co/bibimbap/Qwen-VL-Chat-Int4
WORKDIR Qwen-VL-Chat-Int4

# Install the dependencies from requirements.txt
RUN pip install -r requirements.txt
RUN pip install optimum
RUN pip install auto-gptq

# RUN git clone https://github.com/JustinLin610/AutoGPTQ.git 
# WORKDIR AutoGPTQ
# RUN pip install -v .

WORKDIR /

EXPOSE 3000
CMD tail -f /dev/null 