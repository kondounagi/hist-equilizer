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
        "-o", "--output", required=True, help="Output dir", default="output"
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


if __name__ == "__main__":
    args = get_args()
    os.makedirs(args.output, exist_ok=True)
    input_paths = list(glob(args.include))

    if args.use_clahe:
        clahe = cv2.createCLAHE(
            clipLimit=args.clip_limit,
            tileGridSize=(
                args.tile_grid_size,
                args.tile_grid_size,
            ),
        )

    with alive_bar(len(input_paths)) as bar:
        for input_path in input_paths:
            bar.text(f"Processing {input_path}")
            in_img = cv2.imread(input_path, 0)

            if args.use_clahe:
                out_img = clahe.apply(in_img)
            else:
                out_img = cv2.equalizeHist(in_img)

            output_path = os.path.join(args.output, os.path.split(input_path)[-2])
            bar.text(f"Writing to {output_path}")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cv2.imwrite(output_path, out_img)
            bar()
