import os
import argparse
from glob import glob

import numpy as np
import cv2
from alive_progress import alive_bar


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--include", default="./input", help="Grep expression to include"
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        default="./output",
        help="Output dir",
    )
    parser.add_argument(
        "-l",
        "--limit",
        default=-1,
        type=int,
        help="The maximum number of images to process",
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
    parser.add_argument(
        "--param-search",
        action="store_true",
        help="Generate outputs with various parameters to find best ones",
    )
    return parser.parse_args()


def main(
    use_clahe: bool,
    clip_limit: float,
    tile_grid_size: int,
    include: str,
    output_dir: str,
    limit: int,
):
    os.makedirs(output_dir, exist_ok=True)
    input_paths = list(glob(include))
    if limit != -1:
        input_paths = input_paths[:limit]

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

            base_name = os.path.splitext(os.path.split(input_path)[-2])[0]
            filename = (
                (
                    base_name
                    + f"__CLAHE__clip-limit_{clip_limit}__tile-grid-size_{tile_grid_size}.png"
                )
                if use_clahe
                else (base_name + "__histEqualizer.png")
            )

            output_path = os.path.join(output_dir, filename)
            bar.text(f"Writing to {output_path}")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cv2.imwrite(output_path, out_img)
            bar()


if __name__ == "__main__":
    args = get_args()
    if args.param_search:
        for clip_limit in (1, 2, 4, 8, 10, 20, 40, 80, 160):
            for tile_grid_size in (2, 4, 8, 16, 32, 64, 128, 256, 512):
                print(f"{clip_limit=}, {tile_grid_size=}")
                main(
                    use_clahe=True,
                    clip_limit=clip_limit,
                    tile_grid_size=tile_grid_size,
                    include=args.include,
                    output_dir=args.output_dir,
                    limit=args.limit,
                )
        pass
    else:
        delattr(args, "param_search")
        main(**vars(args))
