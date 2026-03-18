import torch
from diffusers import AutoPipelineForImage2Image
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = AutoPipelineForImage2Image.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float32,
    variant="fp16" if device == "cuda" else None
)

pipe = pipe.to(device)


def generate_wall(image_path, prompt, output_path):

    image = Image.open(image_path).convert("RGB")

    # SDXL Turbo works best with fixed resolution
    image = image.resize((512, 512))

    result = pipe(
        prompt=prompt,
        image=image,
        strength=0.7,
        guidance_scale=0.0,
        num_inference_steps=1,
        height=512,
        width=512
    ).images[0]

    result.save(output_path)

    return output_path