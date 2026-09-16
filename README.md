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
| 2015 | 24 | 64 | [`overview_montage.png`](singapore_2015_tile_10_16/overview_montage.png) | [`singapore_2015_tile_10_16/`](singapore_2015_tile_10_16/) |
| 2020 | 24 | 64 | [`overview_montage.png`](singapore_2020_tile_10_16/overview_montage.png) | [`singapore_2020_tile_10_16/`](singapore_2020_tile_10_16/) |
| 2024 | 24 | 64 | [`overview_montage.png`](singapore_2024_tile_10_16/overview_montage.png) | [`singapore_2024_tile_10_16/`](singapore_2024_tile_10_16/) |

#### One shared layer set (intersection of the three years)

The collection is not uniform over time: 2015 carries 30 modalities, 2020 28 and
2024 24, and six layers stop somewhere in between. Rather than leaving holes in
the comparison, all three folders render the **24 modalities present in all three
years**, so every year has exactly the same 24 panels in exactly the same
positions in an identical **1800 × 1280** 6 × 4 grid, and no panel is a
placeholder. The same 24 layers drive `per_modality/` and `modality_stats.csv` in
every year folder.

The six layers dropped to make that possible, and where they stop:

| layer | available |
|---|---|
| `AirQualityNO2` | 2015 only (stops after 2019) |
| `Electricity Consumption 1km Modelled` | 2015 only (stops after 2019) |
| `LandUse_HILDA` | 2015, 2020 (stops after 2020) |
| `GreenLandCover` | 2015, 2020 (stops after 2022) |
| `AirQualityPM25` | 2015, 2020 (stops after 2023) |
| `BuiltVolume_GHSL` | 2015, 2020 (sparse snapshots) |

They are easy to bring back per year with
`--canonical-from "$CAN"` alone (union mode), which draws grey `(missing)`
placeholders and makes the coverage drift itself the thing you see.

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
    --out singapore_2024_tile_10_16 --canonical-from "$CAN" --canonical-intersect
python scripts/make_location_map.py --tile 10_16 --year 2024 --root $R/2024 \
    --out singapore_2024_tile_10_16/tile_location.png
python scripts/make_readme.py --tile 10_16 --year 2024 --root $R/2024 \
    --out singapore_2024_tile_10_16/README.md
```

Tile identifiers follow the dataset convention `<row>_<col>` (row 0–19 north→south,
col 0–31 west→east), each cell being 2 km × 2 km in EPSG:32648.
