from diffusers import StableDiffusionPipeline
from huggingface_hub import notebook_login
notebook_login()


experimental_pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", revision="fp16", use_auth_token=True)
description_1 = "a photograph of an horse on moon"
image_1 = experimental_pipe(description_1).images[0]
image_1
image_1.save("description_1_based_image.png")

