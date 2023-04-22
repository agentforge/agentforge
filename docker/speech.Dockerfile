FROM historica:latest

RUN pip install llvmlite --ignore-installed && pip install typeguard==2.7.0 TTS inflect
RUN apt-get install -y espeak-ng
RUN pip install git+https://github.com/suno-ai/bark.git
WORKDIR /app/agent_n/historica/speech

# Expose port 3000
EXPOSE 3000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
