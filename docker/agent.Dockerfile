FROM agentforge:latest
ENV RESOURCE=AGENT

# agent
WORKDIR /app/
RUN apt-get install -y python3-dev cmake g++ git make python3

RUN pip install bcrypt pymongo word2number
RUN pip install inflect
RUN pip3 install python-jose
RUN pip install celery pytest-celery asyncio pywebpush
RUN pip install novu bleach graphviz humanize noise stable_baselines3

WORKDIR /app/agentforge/agentforge/api

RUN adduser --disabled-password --gecos '' fragro

# Expose port 3000
EXPOSE 3000
COPY .env /app/agentforge/.env

# CMD API_DOMAIN="https://api.agentforge.ai.ngrok-free.app" WEBSITE_DOMAIN="https://agentforge.ngrok.dev" PYTHONPATH="/app/agentforge/" uvicorn main:app --reload --host=0.0.0.0 --port=3005
CMD tail -f /dev/null
