# hist-equilizer

- You can input both gray and color images.

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

## Input directory structure

```
input
├── 造影画像
│   ├── 40172_20150819_L
│   │   ├── 40172_20150819_115050.023_FA_0056.584_L_22.png
│   │   ├── 40172_20150819_115050.023_FA_0104.230_L_24.png
│   │   ├── 40172_20150819_115050.023_FA_0111.913_L_26.png
│   │   ├── 40172_20150819_115050.023_FA_0234.866_L_28.png
│   │   ├── 40172_20150819_115050.023_FA_0239.926_L_29.png
│   │   ├── 40172_20150819_115050.023_FA_0642.545_L_42.png
│   │   ├── 40172_20150819_115050.023_FA_0656.304_L_43.png
│   │   └── 40172_20150819_115050.023_FA_0702.046_L_44.png
│   ├── 40172_20150819_R
│   │   ├── 40172_20150819_115050.023_FA_0006.693_R_6.png
│   │   ├── 40172_20150819_115050.023_FA_0011.716_R_8.png
│   │   ├── 40172_20150819_115050.023_FA_0015.157_R_10.png
│   │   ├── 40172_20150819_115050.023_FA_0024.142_R_14.png
│   │   ├── 40172_20150819_115050.023_FA_0034.744_R_18.png
│   │   ├── 40172_20150819_115050.023_FA_0043.388_R_20.png
│   │   ├── 40172_20150819_115050.023_FA_0305.105_R_32.png
│   │   ├── 40172_20150819_115050.023_FA_0312.130_R_33.png
│   │   ├── 40172_20150819_115050.023_FA_0321.169_R_34.png
│   │   ├── 40172_20150819_115050.023_FA_0338.378_R_35.png
│   │   ├── 40172_20150819_115050.023_FA_0359.890_R_36.png
│   │   ├── 40172_20150819_115050.023_FA_0554.849_R_37.png
│   │   └── 40172_20150819_115050.023_FA_0559.078_R_38.png
```

## Example

```
python ./hist_equilizer.py -i "./input/造影画像" -o "./output" --use-clahe --clip-limit 8 --tile-grid-size 32
```

## Tips

- Useful parameters
  - FA images from Optos California
    - NPA
      - `--clip-limit 8`
      - `--tile-grid-size 32`
    - NV
      - `--clip-limit 8`
      - `--tile-grid-size 512`
