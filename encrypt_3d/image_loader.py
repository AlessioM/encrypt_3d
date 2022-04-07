from typing import Tuple

import imageio
import numpy as np
from skimage.color import rgb2gray
from skimage.transform import resize


def load_image(source: str, image_size: Tuple[int, int]) -> np.ndarray:
    img = imageio.imread(source)
    if img.ndim > 2:
        img = rgb2gray(img[:, :, :3])
    img = resize(img, image_size)
    img = img > np.max(img) / 2
    return img
