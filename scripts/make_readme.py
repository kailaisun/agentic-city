#!/usr/bin/env python
"""Build README.md for the generated tile visualisation folder."""

import argparse
import csv
import json
import os
from collections import OrderedDict

import geopandas as gpd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tile", default="16_10")
    ap.add_argument("--year", default="2020")
    ap.add_argument("--root", default="/NFS/T5/kailais/agent/Urban-bench/Singapore/2KM/2020")
    ap.add_argument("--out", default="/NFS/T5/kailais/agent/vis_work/singapore_2020_tile_16_10/README.md")
    args = ap.parse_args()

    # tile files are named "<row>_<col>" (row 0..19 north->south, col 0..31 west->east)
    row, col = (int(v) for v in args.tile.split("_"))
    cells = gpd.read_file(f"{args.root}/NDVI_Landsat/cells.geojson")
    ex = cells["parent_centroid_wgs84"].astype(str).str.extract(r"\[\s*([-\d.]+)\s+([-\d.]+)\s*\]")
    cells["lon"] = ex[0].astype(float)
    cells["lat"] = ex[1].astype(float)
    u = cells[["row", "col", "lon", "lat"]].drop_duplicates(["row", "col"])
    r = u[(u["row"] == row) & (u["col"] == col)].iloc[0]

    with open(os.path.join(os.path.dirname(args.out), "modality_stats.csv")) as fh:
        rows = list(csv.DictReader(fh))

    agg = OrderedDict()
    for r_ in rows:
        m = r_["modality"]
        a = agg.setdefault(m, {"bands": 0, "shape": r_["shape"], "unit": r_["unit"],
                               "valid": [], "names": []})
        a["bands"] += 1
        a["valid"].append(float(r_["valid_%"]))
        a["names"].append(r_["band_name"])

    L = []
    L.append("# Singapore 2020 — 2 KM tile `%s` modality visualisation\n" % args.tile)
    L.append(
        "One tile of the **Urban-bench** dataset (source archive `Singapore.tar` from "
        "[`fay-y/Urban-bench`](https://huggingface.co/datasets/fay-y/Urban-bench)) rendered so the "
        "data layout and value distribution of every modality can be inspected at a glance.\n"
    )

    L.append("## Tile\n")
    L.append("| property | value |")
    L.append("|---|---|")
    L.append("| tile id | `%s` (row %d, col %d) |" % (args.tile, row, col))
    L.append("| city / year | Singapore / %s |" % args.year)
    L.append("| size | 2 km × 2 km (512 × 512 px for native rasters) |")
    L.append("| centroid (WGS84) | %.5f, %.5f |" % (r["lon"], r["lat"]))
    L.append("| projected CRS | EPSG:32648 (WGS 84 / UTM zone 48N) |")
    L.append("| location | City Hall / downtown core, Singapore |")
    L.append("| modalities present | %d |\n" % len(agg))

    L.append("## Figures\n")
    L.append("| file | what it shows |")
    L.append("|---|---|")
    L.append("| `overview_montage.png` | all %d modalities side by side (band 1, or RGB for imagery) |" % len(agg))
    L.append("| `per_modality/<name>.png` | every band of one modality, with its own colour scale |")
    L.append("| `tile_location.png` | the 2 KM tile grid of Singapore with this tile highlighted |")
    L.append("| `modality_stats.csv` | per-band min / mean / median / max / valid-pixel fraction |\n")
    L.append("The overview montage uses a **fixed slot per modality** shared with the other "
             "rendered years of this tile, so panels can be compared across years without "
             "hunting for them. Modalities that do not exist for this year are drawn as grey "
             "`(missing)` placeholders instead of shifting the layout, which makes the "
             "coverage drift of the collection directly visible.\n")

    L.append("## Modalities in this tile\n")
    L.append("| modality | bands | raster | unit | band names | valid % |")
    L.append("|---|---|---|---|---|---|")
    for m, a in agg.items():
        names = ", ".join(dict.fromkeys(a["names"]))
        if len(names) > 70:
            names = names[:67] + "..."
        L.append(
            "| `%s` | %d | %s | %s | %s | %.1f |"
            % (m, a["bands"], a["shape"], (a["unit"] or "—")[:38], names or "—",
               sum(a["valid"]) / len(a["valid"]))
        )
    L.append("")

    L.append("## Reading notes\n")
    L.append("- **Rasters at 512 × 512** are the native tile resolution (2 km / 512 ≈ 3.9 m/px metadata grid).")
    L.append("- **Rasters at 2 × 2 or 4 × 4** are coarse, city-scale products (weather, GDP, night lights, "
             "air quality, carbon) that were upsampled to the 2 KM tile grid; each cell holds an "
             "aggregated value, so the panels are annotated with their numbers.")
    L.append("- **`Planet`** bands are R, G, B, alpha (8-bit visual display values); "
             "**`RemoteSensing`** is an 8-bit RGB composite derived from Landsat Collection 2 L2.")
    L.append("- Colour limits use a 2–98 percentile stretch for continuous float bands, with "
             "physical limits where they are known (NDVI −0.2…1.0, LST, etc.).")
    L.append("- `-9999` / non-finite pixels are treated as no-data and masked in grey.")
    L.append("- The `OSM_*` layers are sparse rasterised masks: their declared no-data value is `0`, "
             "meaning *no feature at this pixel*. The `valid %` column therefore reports the share of "
             "the tile that actually carries a feature, so a low value is normal. `OSM_Building` / "
             "`OSM_Amenity` / `OSM_POI` cover ~28 % of this tile, and `Osm` (major highways only) "
             "has no features here at all, although it is populated in 288 of the 640 Singapore tiles.")
    L.append("- `OSM_Address` exists as a modality folder but contains no tiles for 2020.\n")

    L.append("## Reproduce\n")
    L.append("```bash")
    L.append("python make_tile_viz.py --tile %s --year %s" % (args.tile, args.year))
    L.append("python make_location_map.py --tile %s --year %s" % (args.tile, args.year))
    L.append("```")

    with open(args.out, "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("wrote", args.out)


if __name__ == "__main__":
    main()
