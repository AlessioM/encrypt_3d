import numpy as np


def encode_image(key_grid: np.ndarray, img: np.ndarray) -> np.ndarray:
    encoded_image = np.copy(key_grid)
    for y, x in np.ndindex(*img.shape):
        if not img[y, x]:
            pixel_slice = np.s_[y * 2 : y * 2 + 2, x * 2 : x * 2 + 2]
            encoded_image[pixel_slice] = np.logical_not(key_grid[pixel_slice])
    return encoded_image
