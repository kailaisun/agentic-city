# agentic-city

Exploratory visualisations of urban multimodal data for agentic city modelling.

## Contents

### Singapore tile `10_16` — 2015, 2020, 2025

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
| 2025 | 22 | 63 | [`overview_montage.png`](singapore_2025_tile_10_16/overview_montage.png) | [`singapore_2025_tile_10_16/`](singapore_2025_tile_10_16/) |

The modality count drops over the decade because several products have not been
extended past their last release: 2025 has no `Odiac` carbon emission, no air
quality, no `Energy_Electricity` / `Electricity Consumption`, no `Economy_GDP_PPP_1km`,
no `GreenLandCover` and no `LandUse_HILDA`, while 2015 still carries
`AirQualityNO2` and the modelled electricity layer. Comparing the three montages
side by side makes that coverage drift visible. The per-year `README.md` and
`modality_stats.csv` list exactly what is present.

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
python scripts/make_tile_viz.py     --tile 10_16 --year 2025 --root $R/2025 --out singapore_2025_tile_10_16
python scripts/make_location_map.py --tile 10_16 --year 2025 --root $R/2025 --out singapore_2025_tile_10_16/tile_location.png
python scripts/make_readme.py       --tile 10_16 --year 2025 --root $R/2025 --out singapore_2025_tile_10_16/README.md
```

Tile identifiers follow the dataset convention `<row>_<col>` (row 0–19 north→south,
col 0–31 west→east), each cell being 2 km × 2 km in EPSG:32648.
