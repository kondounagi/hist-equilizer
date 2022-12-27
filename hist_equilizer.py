import os
import argparse
from glob import glob

import numpy as np
import cv2
from alive_progress import alive_bar


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-dir", default="./input", help="Path to input images"
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
        "--is-color",
        action="store_true",
        help="When this flag is set to true, input images are processed as color images, not grayscale",
    )
    parser.add_argument(
        "--param-search",
        action="store_true",
        help="Generate outputs with various parameters to find best ones",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
    )
    parser.add_argument(
        "--ext",
        type=str,
        choices=["png", "jpg", "jpeg"],
    )
    return parser.parse_args()


class HistEqualizer(object):
    def __init__(
        self,
        use_clahe: bool,
        clip_limit: float,
        tile_grid_size: int,
        is_color: bool,
        limit: int,
        ext: str,
        **_,
    ):
        self.clahe = (
            cv2.createCLAHE(
                clipLimit=clip_limit,
                tileGridSize=(
                    tile_grid_size,
                    tile_grid_size,
                ),
            )
            if use_clahe
            else None
        )
        self.output_suffix = (
            (f"__CLAHE__clip-limit_{clip_limit}__tile-grid-size_{tile_grid_size}.{ext}")
            if use_clahe
            else f"__histEqualizer.{ext}"
        )
        self.is_color = is_color
        self.limit = limit
        self.ext = ext

    def _hist_equalize_gray(self, img: np.ndarray) -> np.ndarray:
        if self.clahe is not None:
            out_img = self.clahe.apply(img)
        else:
            out_img = cv2.equalizeHist(img)
        return out_img

    def _hist_equalize_color(self, bgr: np.ndarray) -> np.ndarray:
        # ref. https://stackoverflow.com/questions/25008458/how-to-apply-clahe-on-rgb-color-images
        lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
        lab[..., 0] = self._hist_equalize_gray(lab[..., 0])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    def run(self, input_dir: str, output_dir: str, recursive: bool, **_):
        glob_pattern = (
            os.path.join(input_dir, "**", f"*.{self.ext}")
            if recursive
            else os.path.join(input_dir, f"*.{self.ext}")
        )
        print("glob_pattern", glob_pattern)
        png_paths = glob(glob_pattern, recursive=True)
        if self.limit != -1:
            png_paths = png_paths[: self.limit]

        os.makedirs(output_dir, exist_ok=True)

        with alive_bar(len(png_paths)) as bar:
            for png_path in png_paths:
                bar.text(f"Processing {png_path}")

                # if in_img is grayscale
                if not self.is_color:
                    in_img = cv2.imread(png_path, cv2.IMREAD_GRAYSCALE)
                    out_img = self._hist_equalize_gray(in_img)
                    # Presuppose that the directory structure is as follows:
                    # ├───gray_input
                    # │   ├───00176222_20200602_092903.627_COLOR_L_2.png
                    #         ├─SubImage.png
                # if in_img is color
                elif self.is_color:
                    in_img = cv2.imread(png_path, cv2.IMREAD_COLOR)
                    out_img = self._hist_equalize_color(in_img)
                    # Presuppose that the directory structure is as follows:
                    # ├───color_input
                    # │   ├───00176222_20200602_092903.627_COLOR_L_2.png
                else:
                    raise ValueError("Invalid image shape")

                rel_path = os.path.relpath(png_path, input_dir)
                filename = os.path.splitext(rel_path)[0] + self.output_suffix
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
                vars(args)
                he = HistEqualizer(
                    **{
                        **vars(args),
                        "clip_limit": clip_limit,
                        "tile_grid_size": tile_grid_size,
                    }
                )
                he.run(
                    **vars(args),
                )
        pass
    else:
        delattr(args, "param_search")
        he = HistEqualizer(**vars(args))
        he.run(**vars(args))
