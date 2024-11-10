FROM nvidia/cuda:12.1.0-base-ubuntu22.04 AS vllm-base

# libnccl required for ray
RUN apt-get update -y \
    && apt-get install -y python3-pip git

WORKDIR /workspace
COPY requirements.txt requirements.txt
RUN pip install numpy typing_extensions Cython
RUN pip install -r requirements.txt
    
ENV RESOURCE=LLM

WORKDIR /app
RUN pip install outlines[serve]
RUN pip install "pydantic>=2.0"
EXPOSE 8000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD python3 -m outlines.serve.serve --model NousResearch/Meta-Llama-3-8B-Instruct --max-num-batched-tokens 8192
