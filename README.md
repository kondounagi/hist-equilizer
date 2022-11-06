# hist-equilizer

## Prerequisites

```
$ python -V
Python 3.9.13
```

## Environmental Setup

```
$ pip install -r requirements.txt
```

## Usage

```
$ python .\hist_equilizer.py --help
usage: hist_equilizer.py [-h] [-i INCLUDE] [-o OUTPUT_DIR] [-l LIMIT] [--use-clahe]
                         [--clip-limit CLIP_LIMIT] [--tile-grid-size TILE_GRID_SIZE]
                         [--param-search]

optional arguments:
  -h, --help            show this help message and exit
  -i INCLUDE, --include INCLUDE
                        Grep expression to include
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Output dir
  -l LIMIT, --limit LIMIT
                        The maximum number of images to process
  --use-clahe           Use CLAHE instead of histogram equalization
  --clip-limit CLIP_LIMIT
                        CLAHE clip limit (default: 2.0)
  --tile-grid-size TILE_GRID_SIZE
                        CLAHE tile grid size (default: 8)
  --param-search        Generate outputs with various parameters to find best ones
```

## Example

```
python ./hist_equilizer.py -i "./input/**/*.png" -o "./output" --use-clahe --clip-limit 8 --tile-grid-size 32
```

## Memo

- You can input both gray and color images.
