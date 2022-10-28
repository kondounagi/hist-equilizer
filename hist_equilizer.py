import os
import argparse
from glob import glob

import numpy as np
import cv2
from alive_progress import alive_bar


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--include", required=True, help="Grep expression to include"
    )
    parser.add_argument(
        "-o", "--output_dir", required=True, help="Output dir", default="output"
    )
    parser.add_argument(
        "--use-clahe",
        action="store_true",
        help="Use CLAHE instead of histogram equalization",
    )
    parser.add_argument(
        "--clip-limit",
        type=float,
        default=2.0,
        help="CLAHE clip limit (default: 2.0)",
    )
    parser.add_argument(
        "--tile-grid-size",
        type=int,
        default=8,
        help="CLAHE tile grid size (default: 8)",
    )
    return parser.parse_args()


def main(
    use_clahe: bool,
    clip_limit: float,
    tile_grid_size: int,
    include: str,
    output_dir: str,
):
    os.makedirs(output_dir, exist_ok=True)
    input_paths = list(glob(include))

    if use_clahe:
        clahe = cv2.createCLAHE(
            clipLimit=clip_limit,
            tileGridSize=(
                tile_grid_size,
                tile_grid_size,
            ),
        )

    with alive_bar(len(input_paths)) as bar:
        for input_path in input_paths:
            bar.text(f"Processing {input_path}")
            in_img = cv2.imread(input_path, 0)

            if use_clahe:
                out_img = clahe.apply(in_img)
            else:
                out_img = cv2.equalizeHist(in_img)

            output_path = os.path.join(output_dir, os.path.split(input_path)[-2])
            bar.text(f"Writing to {output_path}")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cv2.imwrite(output_path, out_img)
            bar()


if __name__ == "__main__":
    args = get_args()
    main(**vars(args))
