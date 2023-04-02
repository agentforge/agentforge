FROM historica:latest

WORKDIR /app/agent_n/historica/language_model
RUN pip install peft

# Expose port 3000
EXPOSE 3000

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD tail -f /dev/null
