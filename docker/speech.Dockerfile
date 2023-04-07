FROM historica:latest

RUN pip install llvmlite --ignore-installed && pip install typeguard==2.7.0 TTS inflect
RUN apt-get install -y espeak-ng
WORKDIR /app/agent_n/historica/speech

# Expose port 3000
EXPOSE 3000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
