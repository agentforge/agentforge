FROM agentforge:latest
ENV RESOURCE=LLM

RUN pip install peft einops
RUN pip install 'accelerate @ git+https://github.com/huggingface/accelerate.git'
RUN pip install flash-attn==1.0.3.post0
RUN pip install triton==2.0.0.dev20221202
RUN pip install torch==1.13.1
RUN pip install xformers
# Expose port 3000

WORKDIR /app/agentforge/agentforge/api

EXPOSE 3000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
