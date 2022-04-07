import numpy as np
from stl import mesh
from tqdm import tqdm

HOLLOW_BOX_FACES = 8


def hollow_box(
    xmin: float, xmax: float, ymin: float, ymax: float, idx: int, model: mesh.Mesh
) -> int:
    lines = [
        ((xmin, ymin), (xmax, ymin)),
        ((xmax, ymin), (xmax, ymax)),
        ((xmax, ymax), (xmin, ymax)),
        ((xmin, ymax), (xmin, ymin)),
    ]

    for start, stop in lines:

        #
        #  start                  stop
        # 0 +
        #   |
        #   |
        # 1 +----------------------+
        #
        idx += 1
        model.vectors[idx][0] = start + (0,)
        model.vectors[idx][1] = start + (1,)
        model.vectors[idx][2] = stop + (1,)

        #
        #  start                  stop
        # 0 +----------------------+
        #                          |
        #                          |
        # 1                        +
        #
        idx += 1
        model.vectors[idx][0] = start + (0,)
        model.vectors[idx][1] = stop + (0,)
        model.vectors[idx][2] = stop + (1,)

    return idx


NO_HOLE_FACES = 4


def no_hole(
    xmin: float, xmax: float, ymin: float, ymax: float, idx: int, model: mesh.Mesh
) -> int:
    #
    # sub pixel
    #
    # 0:(0,0)                      1:(10,0)
    #
    #
    #
    # 2:(0,10)                     3:(10,10)
    #
    #

    vertices = {
        layer: np.array(
            [
                [xmin, ymin, z],
                [xmax, ymin, z],
                [xmin, ymax, z],
                [xmax, ymax, z],
            ]
        )
        for layer, z in {"bottom": 0, "top": 1}.items()
    }

    faces_flat = np.array(
        [
            [0, 1, 3],
            [0, 3, 2],
        ]
    )

    for layer in ["bottom", "top"]:
        for f in faces_flat:
            idx += 1
            for j in range(3):
                model.vectors[idx][j] = vertices[layer][f[j], :]
    return idx


HOLE_FACES = HOLLOW_BOX_FACES + 16


def hole(
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    idx: int,
    model: mesh.Mesh,
    hole_ratio: float,
) -> int:
    grid_size_x = (xmax - xmin) * hole_ratio
    grid_size_y = (ymax - ymin) * hole_ratio

    xmin_hole = xmin + grid_size_x
    xmax_hole = xmax - grid_size_x
    ymin_hole = ymin + grid_size_y
    ymax_hole = ymax - grid_size_y

    #
    # sub pixel
    #
    # 0:(0,0)                      1:(10,0)
    #
    #      4:(2,2) ---------  5:(8,2)
    #          |                |
    #          |                |
    #      6: (2,8) --------- 7:(8,8)
    #
    # 2:(0,10)                     3:(10,10)
    #
    #

    vertices = {
        layer: np.array(
            [
                [xmin, ymin, z],
                [xmax, ymin, z],
                [xmin, ymax, z],
                [xmax, ymax, z],
                [xmin_hole, ymin_hole, z],
                [xmax_hole, ymin_hole, z],
                [xmin_hole, ymax_hole, z],
                [xmax_hole, ymax_hole, z],
            ]
        )
        for layer, z in {"bottom": 0, "top": 1}.items()
    }

    faces_flat = np.array(
        [
            [0, 1, 5],
            [0, 5, 4],
            [0, 4, 2],
            [2, 4, 6],
            [2, 6, 7],
            [2, 7, 3],
            [1, 3, 5],
            [3, 7, 5],
        ]
    )

    for layer in ["bottom", "top"]:
        for f in faces_flat:
            idx += 1
            for j in range(3):
                model.vectors[idx][j] = vertices[layer][f[j], :]

    idx = hollow_box(
        xmin=xmin_hole,
        xmax=xmax_hole,
        ymin=ymin_hole,
        ymax=ymax_hole,
        idx=idx,
        model=model,
    )
    return idx


def grid_to_mesh(grid: np.ndarray, hole_ratio: float) -> mesh.Mesh:
    sub_pixel_count = grid.shape[0] * grid.shape[1]

    # each pixel consits of exactly two holes and two non hole subpixels
    total_face_count = (
        int(sub_pixel_count / 2) * HOLE_FACES
        + int(sub_pixel_count / 2) * NO_HOLE_FACES
        + HOLLOW_BOX_FACES
    )

    model = mesh.Mesh(np.zeros(total_face_count, dtype=mesh.Mesh.dtype))
    idx = -1
    for ymin, xmin in tqdm(np.ndindex(*grid.shape)):
        if grid[ymin, xmin]:
            idx = hole(
                xmin=xmin,
                xmax=xmin + 1,
                ymin=ymin,
                ymax=ymin + 1,
                idx=idx,
                model=model,
                hole_ratio=hole_ratio,
            )
        else:
            idx = no_hole(
                xmin=xmin, xmax=xmin + 1, ymin=ymin, ymax=ymin + 1, idx=idx, model=model
            )

    idx = hollow_box(
        xmin=0,
        xmax=grid.shape[1] + 1,
        ymin=0,
        ymax=grid.shape[0] + 1,
        idx=idx,
        model=model,
    )
    return model
