#!/usr/bin/env python
"""Draw the Singapore 2KM tile grid and highlight the tile used for the visualisation."""

import argparse

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tile", default="16_10")
    ap.add_argument("--year", default="2020")
    ap.add_argument("--root", default="/NFS/T5/kailais/agent/Urban-bench/Singapore/2KM/2020")
    ap.add_argument("--out", default="/NFS/T5/kailais/agent/vis_work/singapore_2020_tile_16_10/tile_location.png")
    args = ap.parse_args()

    # tile files are named "<row>_<col>" (row 0..19 north->south, col 0..31 west->east)
    row, col = (int(v) for v in args.tile.split("_"))
    cells = gpd.read_file(f"{args.root}/NDVI_Landsat/cells.geojson")
    cells = cells[["row", "col", "geometry"]].drop_duplicates(["row", "col"])
    cells_wgs = cells.to_crs(4326)
    sel = cells_wgs[(cells_wgs["row"] == row) & (cells_wgs["col"] == col)]

    fig, ax = plt.subplots(figsize=(11, 8))
    cells_wgs.plot(ax=ax, facecolor="#eef3f7", edgecolor="#c8d4dd", linewidth=0.35)
    sel.plot(ax=ax, facecolor="#e8443a", edgecolor="#7a1410", linewidth=1.6)

    if len(sel):
        c = sel.geometry.iloc[0].centroid
        ax.annotate(
            f"tile {args.tile}\n(lon {c.x:.4f}, lat {c.y:.4f})",
            xy=(c.x, c.y), xytext=(c.x - 0.075, c.y + 0.055),
            fontsize=11, fontweight="bold", color="#7a1410",
            arrowprops=dict(arrowstyle="->", color="#7a1410", lw=1.4),
        )

    ax.set_title(
        f"Urban-bench 2KM tile grid — Singapore {args.year}\n"
        f"highlighted: tile {args.tile} (2 km x 2 km, UTM 48N / EPSG:32648)",
        fontsize=13,
    )
    ax.set_xlabel("longitude")
    ax.set_ylabel("latitude")
    ax.grid(alpha=0.25, linewidth=0.4)
    fig.tight_layout()
    fig.savefig(args.out, dpi=130)
    print("saved", args.out)


if __name__ == "__main__":
    main()
