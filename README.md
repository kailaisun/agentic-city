# agentic-city

Exploratory visualisations of urban multimodal data for agentic city modelling.

## Contents

### [`singapore_2020_tile_10_16/`](singapore_2020_tile_10_16/)

Every modality of a single **2 km tile** of Singapore for **2020** from the
[`fay-y/Urban-bench`](https://huggingface.co/datasets/fay-y/Urban-bench) dataset
(`Singapore.tar`), rendered so the data layout and value distributions can be
inspected at a glance.

The tile sits over the City Hall / downtown core (lon 103.858, lat 1.294) and
contains **28 modalities / 70 bands** — optical imagery (Planet, Landsat),
elevation and building height, population and built volume, land cover, land
surface temperature, weather, night lights, air quality, property values and
OpenStreetMap layers.

| file | what it shows |
|---|---|
| [`overview_montage.png`](singapore_2020_tile_10_16/overview_montage.png) | all 28 modalities side by side |
| [`tile_location.png`](singapore_2020_tile_10_16/tile_location.png) | where the tile sits in Singapore |
| [`per_modality/`](singapore_2020_tile_10_16/per_modality/) | one figure per modality, all bands |
| [`modality_stats.csv`](singapore_2020_tile_10_16/modality_stats.csv) | per-band min / mean / median / max / valid fraction |
| [`README.md`](singapore_2020_tile_10_16/README.md) | modality table, units and reading notes |

### [`scripts/`](scripts/)

Reproducible generators for the figures above:

```bash
python scripts/make_tile_viz.py     --tile 10_16 --year 2020
python scripts/make_location_map.py --tile 10_16 --year 2020
python scripts/make_readme.py       --tile 10_16 --year 2020
```

Tile identifiers follow the dataset convention `<row>_<col>` (row 0–19 north→south,
col 0–31 west→east), each cell being 2 km × 2 km in EPSG:32648.
