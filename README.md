# agentic-city

Exploratory visualisations of urban multimodal data for agentic city modelling.

## Contents

### Singapore tile `10_16` — 2015, 2020, 2024

Every modality of a single **2 km tile** of Singapore, rendered for three years
from the
[`fay-y/Urban-bench`](https://huggingface.co/datasets/fay-y/Urban-bench) dataset
(`Singapore.tar`), rendered so the data layout and value distributions can be
inspected at a glance.

The tile sits over the City Hall / downtown core (lon 103.858, lat 1.294) and
each year covers optical imagery (Planet, Landsat),
elevation and building height, population and built volume, land cover, land
surface temperature, weather, night lights, air quality, property values and
OpenStreetMap layers.

| year | modalities | bands | montage | folder |
|---|---|---|---|---|
| 2015 | 30 | 72 | [`overview_montage.png`](singapore_2015_tile_10_16/overview_montage.png) | [`singapore_2015_tile_10_16/`](singapore_2015_tile_10_16/) |
| 2020 | 28 | 70 | [`overview_montage.png`](singapore_2020_tile_10_16/overview_montage.png) | [`singapore_2020_tile_10_16/`](singapore_2020_tile_10_16/) |
| 2024 | 24 | 64 | [`overview_montage.png`](singapore_2024_tile_10_16/overview_montage.png) | [`singapore_2024_tile_10_16/`](singapore_2024_tile_10_16/) |

#### The three montages are slot-aligned

All three use the same **1800 × 1600** layout with **one fixed grid position per
modality**, taken from the union of the three years. A modality that does not
exist for a given year is drawn as a grey `(missing)` placeholder rather than
disappearing and shifting everything after it, so the same panel can be compared
across years without hunting for it. The banner states how many of the 30 slots
that year actually fills.

This also makes the coverage drift of the collection readable at a glance. 2015
fills all 30 slots; 2020 is missing `AirQualityNO2` and
`Electricity Consumption 1km Modelled`; 2024 is missing six — `AirQualityNO2`,
`AirQualityPM25`, `BuiltVolume_GHSL`,
`Electricity Consumption 1km Modelled`, `GreenLandCover` and `LandUse_HILDA` —
because those products were not extended past their last release. The per-year
`README.md` and `modality_stats.csv` list exactly what is present.

Each year folder contains the same set of files:

| file | what it shows |
|---|---|
| `overview_montage.png` | every modality of that year side by side |
| `tile_location.png` | where the tile sits in Singapore |
| `per_modality/` | one figure per modality, all bands |
| `modality_stats.csv` | per-band min / mean / median / max / valid fraction |
| `README.md` | modality table, units and reading notes |

### [`scripts/`](scripts/)

Reproducible generators for the figures above:

```bash
R=/path/to/Urban-bench/Singapore/2KM
CAN="$R/2015,$R/2020,$R/2024"          # shared slot order across all three years
python scripts/make_tile_viz.py --tile 10_16 --year 2024 --root $R/2024 \
    --out singapore_2024_tile_10_16 --canonical-from "$CAN"
python scripts/make_location_map.py --tile 10_16 --year 2024 --root $R/2024 \
    --out singapore_2024_tile_10_16/tile_location.png
python scripts/make_readme.py --tile 10_16 --year 2024 --root $R/2024 \
    --out singapore_2024_tile_10_16/README.md
```

Tile identifiers follow the dataset convention `<row>_<col>` (row 0–19 north→south,
col 0–31 west→east), each cell being 2 km × 2 km in EPSG:32648.
