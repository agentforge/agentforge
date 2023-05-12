FROM agentforge:latest

RUN apt-get install -y espeak-ng
RUN pip install typeguard==2.7.0 TTS inflect --ignore-installed llvmlite
RUN pip install git+https://github.com/suno-ai/bark.git
RUN pip uninstall -y psutil
RUN pip uninstall -y urllib3 && pip install urllib3==1.26
WORKDIR /app/agent_n/agentforge/speech

# Expose port 3000
EXPOSE 3000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
