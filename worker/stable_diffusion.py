from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")

# disable the following line if you run on CPU
pipe = pipe.to("cuda")

def dummy(images, **kwargs):
  return images, False

pipe.safety_checker = dummy

prompt = "a photo of an astronaut riding a horse on mars"
image = pipe(prompt).images[0]  
    
image.save("test.png")