from models.light_diffusion_model import generate_wall

generate_wall(
    "wall.jpeg",
    "a living room wall painted light blue",
    "output.png"
)

print("Image generated")