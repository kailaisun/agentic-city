# Singapore 2020 — 2 KM tile `10_16` modality visualisation

One tile of the **Urban-bench** dataset (source archive `Singapore.tar` from [`fay-y/Urban-bench`](https://huggingface.co/datasets/fay-y/Urban-bench)) rendered so the data layout and value distribution of every modality can be inspected at a glance.

## Tile

| property | value |
|---|---|
| tile id | `10_16` (row 10, col 16) |
| city / year | Singapore / 2015 |
| size | 2 km × 2 km (512 × 512 px for native rasters) |
| centroid (WGS84) | 103.85847, 1.29351 |
| projected CRS | EPSG:32648 (WGS 84 / UTM zone 48N) |
| location | City Hall / downtown core, Singapore |
| modalities present | 30 |

## Figures

| file | what it shows |
|---|---|
| `overview_montage.png` | all 30 modalities side by side (band 1, or RGB for imagery) |
| `per_modality/<name>.png` | every band of one modality, with its own colour scale |
| `tile_location.png` | the 2 KM tile grid of Singapore with this tile highlighted |
| `modality_stats.csv` | per-band min / mean / median / max / valid-pixel fraction |

## Modalities in this tile

| modality | bands | raster | unit | band names | valid % |
|---|---|---|---|---|---|
| `AirQualityNO2` | 1 | 2x2 | — | band 1 | 100.0 |
| `AirQualityPM25` | 1 | 2x2 | — | band 1 | 100.0 |
| `BuildingHeight_3DGloBFP` | 1 | 512x512 | — | band 1 | 100.0 |
| `BuiltVolume_GHSL` | 2 | 512x512 | — | total built-volume density, m3/m2, non-residential built-volume den... | 100.0 |
| `DEM` | 1 | 512x512 | — | band 1 | 100.0 |
| `Economic_Property` | 4 | 512x512 | SGD | property_value_median_local_currency, property_value_mean_local_cur... | 100.0 |
| `Economic_Property_2017ppp_gdp` | 4 | 512x512 | SGD | property_value_median_local_currency, property_value_mean_local_cur... | 100.0 |
| `Economy_GDP_PPP_1km` | 1 | 2x2 | — | band 1 | 100.0 |
| `Electricity Consumption 1km Modelled` | 1 | 2x2 | kWh/km2/year | band 1 | 100.0 |
| `Energy_Electricity` | 1 | 4x4 | kWh/account/500m_cell/year | band 1 | 100.0 |
| `GreenLandCover` | 2 | 512x512 | — | raw fine land-cover class, green group: 0 non-green, 1 tree, 2 shru... | 100.0 |
| `Height` | 1 | 512x512 | m | band 1 | 100.0 |
| `LandUse_HILDA` | 1 | 512x512 | — | band 1 | 100.0 |
| `NDVI_Landsat` | 1 | 512x512 | unitless NDVI [-1,1] | band 1 | 89.5 |
| `NDVI_MODIS` | 1 | 512x512 | unitless NDVI [-1,1] | band 1 | 100.0 |
| `NighttimeLights` | 1 | 4x4 | nW/cm2/sr | band 1 | 100.0 |
| `OSM_Amenity` | 1 | 512x512 | — | band 1 | 32.5 |
| `OSM_Building` | 1 | 512x512 | — | band 1 | 100.0 |
| `OSM_POI` | 1 | 512x512 | — | band 1 | 100.0 |
| `OSM_Transportation` | 1 | 512x512 | — | band 1 | 100.0 |
| `Odiac` | 1 | 2x2 | tonne carbon per 1 km cell per year | band 1 | 100.0 |
| `Osm` | 1 | 512x512 | — | band 1 | 4.9 |
| `Planet` | 4 | 512x512 | none | red visual display value, green visual display value, blue visual d... | 100.0 |
| `Population_GHSL` | 1 | 512x512 | population count per native GHSL grid  | band 1 | 100.0 |
| `RemoteSensing` | 3 | 512x512 | 8-bit RGB derived from Landsat Collect | band 1, band 2, band 3 | 99.5 |
| `Temperature_LandsatST` | 7 | 512x512 | degree Celsius for LST bands | lst_mean_celsius, lst_median_celsius, lst_p90_celsius, lst_p95_cels... | 100.0 |
| `Temperature_MODISLST` | 7 | 512x512 | degree Celsius for LST bands | lst_mean_celsius, lst_median_celsius, lst_p90_celsius, lst_p95_cels... | 100.0 |
| `Weather_CHELSA_daily` | 9 | 2x2 | — | TMIN, TMAX, TMEAN, PRCP, SRAD, RH, WIND, PRESSURE, CLOUD | 100.0 |
| `Weather_terraclimate` | 10 | 2x2 | — | TMIN, TMAX, TMEAN, PRCP, SRAD, VP, RH_DERIVED, WS, SWE, SWE_MAX | 100.0 |
| `nightlight_MVNL` | 1 | 4x4 | nW cm-2 sr-1 | band 1 | 100.0 |

## Reading notes

- **Rasters at 512 × 512** are the native tile resolution (2 km / 512 ≈ 3.9 m/px metadata grid).
- **Rasters at 2 × 2 or 4 × 4** are coarse, city-scale products (weather, GDP, night lights, air quality, carbon) that were upsampled to the 2 KM tile grid; each cell holds an aggregated value, so the panels are annotated with their numbers.
- **`Planet`** bands are R, G, B, alpha (8-bit visual display values); **`RemoteSensing`** is an 8-bit RGB composite derived from Landsat Collection 2 L2.
- Colour limits use a 2–98 percentile stretch for continuous float bands, with physical limits where they are known (NDVI −0.2…1.0, LST, etc.).
- `-9999` / non-finite pixels are treated as no-data and masked in grey.
- The `OSM_*` layers are sparse rasterised masks: their declared no-data value is `0`, meaning *no feature at this pixel*. The `valid %` column therefore reports the share of the tile that actually carries a feature, so a low value is normal. `OSM_Building` / `OSM_Amenity` / `OSM_POI` cover ~28 % of this tile, and `Osm` (major highways only) has no features here at all, although it is populated in 288 of the 640 Singapore tiles.
- `OSM_Address` exists as a modality folder but contains no tiles for 2020.

## Reproduce

```bash
python make_tile_viz.py --tile 10_16 --year 2015
python make_location_map.py --tile 10_16 --year 2015
```
