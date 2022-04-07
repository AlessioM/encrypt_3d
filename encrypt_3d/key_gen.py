import itertools
from typing import Tuple

import numpy as np
from numpy.random import MT19937, RandomState, SeedSequence
from tqdm import tqdm


def generate_key_grid(grid_size: Tuple[int, int], key: int) -> np.ndarray:
    # each pixel is represented by 4 subpixel
    sub_pixels = np.arange(4)
    sub_pixel_loc = np.array(list(np.ndindex(2, 2)))

    # each pixel has exacctly two sub pixels "set to black"
    valid_pixels = np.array(list(itertools.permutations(sub_pixels, 2)))

    # use the key as random seed
    rs = RandomState(MT19937(SeedSequence(key)))
    key_img = rs.randint(0, valid_pixels.shape[0], size=grid_size)

    key_grid = np.zeros(np.array(key_img.shape) * 2, dtype=bool)

    # set the subpixel corresponding to the key
    pixel_pos = np.ndindex(*grid_size)
    for p in tqdm(pixel_pos):
        sub_pixels_to_set = valid_pixels[key_img[p]]
        pixels_to_set = sub_pixel_loc[sub_pixels_to_set] + np.array(p) * 2
        for s in pixels_to_set:
            key_grid[s[0], s[1]] = True

    return key_grid
