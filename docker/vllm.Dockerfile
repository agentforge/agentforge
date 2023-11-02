FROM nvcr.io/nvidia/pytorch:22.12-py3
ENV RESOURCE=LLM

WORKDIR /app
RUN git clone https://github.com/vllm-project/vllm.git && cd vllm && pip install -e .
EXPOSE 8000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
