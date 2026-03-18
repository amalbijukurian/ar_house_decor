import torch
from diffusers import AutoPipelineForImage2Image
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = AutoPipelineForImage2Image.from_pretrained(
    "SimianLuo/LCM_Dreamshaper_v7",
    torch_dtype=torch.float32
)

pipe = pipe.to(device)
pipe.enable_attention_slicing()


def generate_wall(image_path, color, output_path):

    image = Image.open(image_path).convert("RGB")
    image = image.resize((512,512))

    prompt = f"a realistic living room wall painted {color}"

    result = pipe(
        prompt=prompt,
        image=image,
        strength=0.7,
        num_inference_steps=4,
        guidance_scale=1
    ).images[0]

    result.save(output_path)

    return output_path