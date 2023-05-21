FROM agentforge:latest

WORKDIR /app/agentforge/agentforge/language_model
RUN pip install peft einops
RUN pip install 'accelerate @ git+https://github.com/huggingface/accelerate.git'
RUN pip install flash-attn==1.0.3.post0
RUN pip install triton==2.0.0.dev20221202
# Expose port 3000
EXPOSE 3000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
