FROM agentforge:latest
ENV RESOURCE=AGENT

# agent
WORKDIR /app/
RUN apt-get install -y python3-dev cmake g++ git make python3

# Install Fast Downward -- Classical Planning
RUN apt-get update && apt install g++-10 && apt-get install build-essential gdb && \
    update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 40 && \
    update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 60 && \
    update-alternatives --config g++ && \
    git clone https://github.com/aibasel/downward.git && \
    cd downward && mkdir -p builds/main && \
    cd builds/main && \
    cmake ../../src DCMAKE_BUILD_TYPE=RELEASE && \
    make

RUN pip install bcrypt pymongo word2number
RUN pip install inflect
RUN pip install twilio 
RUN pip3 install python-jose
RUN pip install celery pytest-celery asyncio pywebpush
RUN pip install novu bleach

WORKDIR /app/agentforge/agentforge/api

# Expose port 3000
EXPOSE 3000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
