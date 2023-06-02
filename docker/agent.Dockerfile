FROM agentforge:latest

# agent
WORKDIR /app/agentforge/agentforge/agent
RUN apt-get install -y python3-dev
RUN pip install bcrypt pymongo
RUN pip install inflect
# Expose port 3000
EXPOSE 3000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
