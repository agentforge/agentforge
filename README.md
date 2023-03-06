# agent_n

To build the Docker image, run the following command:

```docker build --build-arg REPO_URL=git@github.com:fragro/elder-link.git  --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" -t worker .```

To run the Docker container, run the following command:

```nvidia-docker run --ipc=host -p 3000:3000 worker .```

To run an interactive shell use this instead:

```nvidia-docker run -it --ipc=host -p 3000:3000 worker /bin/bash```

To run the flask server:

```flask run --host=0.0.0.0 --port=3000```

To run the rails server

```rails server -p 3001```

## Installing Stable Diffusion

Docker doesn't work because realesrgan doesn't work in VM
TODO: Convert to non-dockerfile

```
# Stable Diffusion - 
# Stable Diffusion - Fun Times
RUN git clone git@github.com:CompVis/stable-diffusion.git
RUN git clone git@github.com:jquesnelle/txt2imghd.git

RUN pip install gTTS flask pytest accelerate bitsandbytes trl
RUN pip install --upgrade diffusers[torch]
RUN apt-get update && apt-get install -y git openssh-client

RUN . /root/.bashrc && \
    conda init bash && \
    conda env create -f stable-diffusion/environment.yaml && \
    conda update -n base condastable-diffusion-

RUN wget -P /app/cache/ https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt
RUN wget -P /app/cache/ https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-ubuntu.zip

RUN mkdir -p /root/stable-diffusion/models/ldm/stable-diffusion-v1
RUN ln -s /app/cache/v1-5-pruned-emaonly.ckpt /root/stable-diffusion/models/ldm/stable-diffusion-v1/model.ckpt

WORKDIR /app/stable-diffusion
RUN unzip /app/cache/realesrgan-ncnn-vulkan-20220424-ubuntu.zip
RUN chmod +x un Times
RUN git clone git@github.com:CompVis/stable-diffusion.git
RUN git clone git@github.com:jquesnelle/txt2imghd.git

RUN pip install gTTS flask pytest accelerate bitsandbytes trl
RUN pip install --upgrade diffusers[torch]
RUN apt-get update && apt-get install -y git openssh-client

RUN . /root/.bashrc && \
    conda init bash && \
    conda env create -f stable-diffusion/environment.yaml && \
    conda update -n base condastable-diffusion-

RUN wget -P /app/cache/ https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt
RUN wget -P /app/cache/ https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-ubuntu.zip

RUN mkdir -p /root/stable-diffusion/models/ldm/stable-diffusion-v1
RUN ln -s /app/cache/v1-5-pruned-emaonly.ckpt /root/stable-diffusion/models/ldm/stable-diffusion-v1/model.ckpt

WORKDIR /app/stable-diffusion
RUN unzip /app/cache/realesrgan-ncnn-vulkan-20220424-ubuntu.zip
RUN chmod +x 

intricate Three-point lighting portrait, by Ching Yeh and Greg Rutkowski, detailed cyberpunk in the style of GitS 1995
pip install 'torchmetrics<0.8'
tulsa, art deco, neon lights, tone mapped, shiny, intricate, cinematic lighting, highly detailed, digital painting, artstation, concept art, smooth, sharp focus, illustration

a humanoid armored futuristic cybernetic samurai with glowing neon decals, award winning photograph, close up, focused trending on artstation, octane render, portrait, hyperrealistic, ultra detailed, photograph

In 2070 or so Tenements on fire Blazing through endless nights And behind every spy hole Car wrecks and barbed wire Dirty streets and knife fights

concept art of a far-future city, key visual, summer day, highly detailed, digital painting, artstation, concept art, sharp focus, in harmony with nature, streamlined, by makoto shinkai and akihiko yoshida and hidari and wlop

Through every forest Above the trees Within my stomach Scraped off my knees I drink the honey Inside your hive You are the reason I stay alive, gothic, black and white, bees, nectar, fruit, rotting, drinking, sucking, spixtting, photograph, polaroid

shrimp boat parked merrily in the galveston docks, 1976, photorealistic, nikon, award winning photograph, close up, focused trending on artstation, octane render, portrait, hyperrealistic, ultra detailed, photograph

The battle for Benghazi, the victorious muslims overtake the CIA and evil amerikkans as they fire missiles into the American Embassy, Takbir, , photorealistic, nikon, award winning photograph, close up, focused trending on artstation, octane render, portrait, hyperrealistic, ultra detailed, photograph

photo realistic portrait of young woman, red hair, pale, realistic eyes, gold necklace with big ruby, centered in frame, facing camera, symmetrical face, ideal human, 85mm lens,f8, photography, ultra details, natural light, dark background, photo, out of focus trees in background –ar 9:16 –testp –v 3 –upbeta

```
