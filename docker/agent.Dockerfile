FROM agentforge:latest
ENV RESOURCE=AGENT

# agent
WORKDIR /app/
RUN apt-get install -y python3-dev cmake g++ git make python3

# Install Fast Downward -- Classical Planning
RUN git clone https://github.com/aibasel/downward.git && \
    cd downward && mkdir -p builds/main && \
    cd builds/main && \
    cmake ../../src DCMAKE_BUILD_TYPE=RELEASE && \
    make

RUN pip install bcrypt pymongo
RUN pip install inflect
RUN pip install twilio
RUN pip3 install python-jose


WORKDIR /app/agentforge/agentforge/api

# Expose port 3000
EXPOSE 3000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
