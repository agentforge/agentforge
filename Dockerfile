# Use the huggingface/transformers-pytorch-deepspeed-latest-gpu-push-ci image as the base image
FROM huggingface/transformers-pytorch-deepspeed-latest-gpu-push-ci

RUN pip install gTTS flask

# Copy the cacher file to the container
COPY cache.py /app/

# Set the working directory to /app
WORKDIR /app

# Cache the trained model
RUN python cache.py

RUN pip install pytest

COPY cache-whisper.py /app/
RUN python cache-whisper.py

# Copy over remaining libs
COPY app.py /app/
COPY speech /app/speech
COPY inference /app/inference

# Expose port 3000
EXPOSE 3000

# Run the Flask API
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]