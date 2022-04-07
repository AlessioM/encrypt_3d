import click

from encrypt_3d.image_encoder import encode_image
from encrypt_3d.image_loader import load_image
from encrypt_3d.key_gen import generate_key_grid
from encrypt_3d.mesh_gen import grid_to_mesh

from .config import cfg


@click.group()
@click.version_option()
@click.option("--key", required=True, type=int)
@click.option("--grid-width", default=cfg.grid_width, type=click.IntRange(2, None))
@click.option("--grid-height", default=cfg.grid_height, type=click.IntRange(2, None))
@click.option("--hole-ratio", default=cfg.hole_ratio, type=click.FloatRange(0, 1))
def command_line(
    key: int, grid_width: int, grid_height: int, hole_ratio: float
) -> None:
    """generate 'encrypted' 3D images"""
    cfg.key = key
    cfg.grid_width = grid_width
    cfg.grid_height = grid_height
    cfg.hole_ratio = hole_ratio


@command_line.command()
@click.option(
    "--key-output", type=click.Path(file_okay=True, writable=True), required=True
)
def generate_key(key_output: str) -> None:
    key_grid = generate_key_grid((cfg.grid_height, cfg.grid_width), cfg.key)
    key_grid_mesh = grid_to_mesh(key_grid, cfg.hole_ratio)
    key_grid_mesh.save(key_output)


@command_line.command()
@click.option("--image-input", required=True)
@click.option(
    "--image-output", type=click.Path(file_okay=True, writable=True), required=True
)
def encode(image_input: str, image_output: str) -> None:
    key_grid = generate_key_grid((cfg.grid_height, cfg.grid_width), cfg.key)
    img = load_image(image_input, (cfg.grid_height, cfg.grid_width))
    encoded_image = encode_image(key_grid, img)
    encoded_image_mesh = grid_to_mesh(encoded_image, cfg.hole_ratio)
    encoded_image_mesh.save(image_output)
