#!/usr/bin/env python
"""
Visualise every modality of one Urban-bench 2KM tile (Singapore, 2020).

Produces, under --out:
  overview_montage.png      one panel per modality
  per_modality/<name>.png   all bands of a modality
  tile_location.png         where the tile sits inside Singapore
  modality_stats.csv        per-band statistics
  README.md                 index of the generated figures
"""

import argparse
import csv
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from matplotlib.colors import Normalize

# ---------------------------------------------------------------- styling ----

# modality -> (colormap, vmin, vmax); None means auto percentile stretch
STYLE = {
    "NDVI_Landsat": ("RdYlGn", -0.2, 1.0),
    "NDVI_MODIS": ("RdYlGn", -0.2, 1.0),
    "DEM": ("terrain", None, None),
    "Height": ("terrain", None, None),
    "BuildingHeight_3DGloBFP": ("magma", 0, None),
    "Population_GHSL": ("viridis", 0, None),
    "BuiltVolume_GHSL": ("cividis", 0, None),
    "NighttimeLights": ("inferno", 0, None),
    "nightlight_MVNL": ("inferno", 0, None),
    "Temperature_LandsatST": ("inferno", None, None),
    "Temperature_MODISLST": ("inferno", None, None),
    "LandUse_HILDA": ("tab20", None, None),
    "GreenLandCover": ("YlGn", None, None),
    "OSM_Building": ("Greys", 0, 1),
    "OSM_Amenity": ("Greys", 0, 1),
    "OSM_POI": ("Greys", 0, 1),
    "OSM_Address": ("Greys", 0, 1),
    "Osm": ("Greys", None, None),
    "OSM_Transportation": ("Greys", 0, 1),
    "Economic_Property": ("plasma", 0, None),
    "Economic_Property_2017ppp_gdp": ("plasma", 0, None),
    "Energy_Electricity": ("cividis", 0, None),
    "Economy_GDP_PPP_1km": ("cividis", 0, None),
    "AirQualityPM25": ("YlOrBr", 0, None),
    "Odiac": ("YlGnBu", None, None),
    "Weather_terraclimate": ("coolwarm", None, None),
    "Weather_CHELSA_daily": ("coolwarm", None, None),
}

RGB_MODALITIES = {"Planet": (1, 2, 3), "RemoteSensing": (1, 2, 3)}

# datasets stored on a coarser native grid (whole-city value per coarse cell)
COARSE = 16


# ----------------------------------------------------------------- helpers ----


def band_names(modality, count, meta):
    """Best-effort band labels from the dataset metadata."""
    for key in ("bands", "band_semantics", "band_names", "source_tile_bands"):
        b = meta.get(key)
        if isinstance(b, list) and b:
            names = []
            for item in b:
                if isinstance(item, dict):
                    names.append(str(item.get("variable") or item.get("band") or ""))
                else:
                    names.append(str(item))
            if len(names) >= count:
                return names[:count]
    return [f"band {i + 1}" for i in range(count)]


def load_meta(mod_dir):
    meta = {}
    md = os.path.join(mod_dir, "metadata")
    for f in ("metadata.json", "temporal_status.json"):
        p = os.path.join(md, f)
        if os.path.isfile(p):
            try:
                with open(p) as fh:
                    meta.update(json.load(fh))
            except Exception:
                pass
    return meta


def read_band(path, idx):
    with rasterio.open(path) as src:
        a = src.read(idx).astype("float32")
        nodata = src.nodata
    # sentinel / non-physical values used across the collection
    a[~np.isfinite(a)] = np.nan
    a[a <= -9999] = np.nan
    if nodata is not None and np.isfinite(nodata):
        a[a == nodata] = np.nan
    return a


def robust(a, lo=2, hi=98):
    v = a[np.isfinite(a)]
    if v.size == 0:
        return 0.0, 1.0
    return float(np.percentile(v, lo)), float(np.percentile(v, hi))


def draw_raster(ax, a, cmap, vmin, vmax, title=""):
    if vmin is None or vmax is None:
        vmin, vmax = robust(a)
    if vmin == vmax:
        vmax = vmin + 1
    cm = plt.get_cmap(cmap).copy()
    cm.set_bad("#f0f0f0")
    im = ax.imshow(a, cmap=cm, vmin=vmin, vmax=vmax, interpolation="nearest")
    ax.set_title(title, fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])
    return im


def draw_coarse(ax, a, cmap, vmin, vmax, title=""):
    """Coarse grids: show the values as an annotated heatmap."""
    if vmin is None or vmax is None:
        vmin, vmax = robust(a)
    if vmin == vmax:
        vmax = vmin + 1
    im = ax.imshow(a, cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest")
    h, w = a.shape
    if h * w <= 64:
        for i in range(h):
            for j in range(w):
                if np.isfinite(a[i, j]):
                    ax.text(
                        j, i, f"{a[i, j]:.3g}",
                        ha="center", va="center", fontsize=6, color="black",
                    )
    ax.set_title(title, fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])
    return im


# -------------------------------------------------------------------- main ----


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tile", default="16_10")
    ap.add_argument("--year", default="2020")
    ap.add_argument("--root", default="/NFS/T5/kailais/agent/Urban-bench/Singapore/2KM/2020")
    ap.add_argument("--out", default="/NFS/T5/kailais/agent/vis_work/singapore_2020_tile_16_10")
    args = ap.parse_args()

    os.makedirs(os.path.join(args.out, "per_modality"), exist_ok=True)
    mods = sorted(d for d in os.listdir(args.root) if os.path.isdir(os.path.join(args.root, d)))

    panels, rows = [], []
    for m in mods:
        tif = os.path.join(args.root, m, "data", f"{args.tile}_s2km_y{args.year}.tif")
        if not os.path.isfile(tif):
            continue
        meta = load_meta(os.path.join(args.root, m))
        unit = str(meta.get("unit") or meta.get("units") or "").split(";")[0].strip()

        with rasterio.open(tif) as src:
            count = src.count
            small = src.width <= COARSE

        # ---- per-modality figure (all bands) ----
        fig, axes = plt.subplots(1, count, figsize=(3.6 * count, 4.0), squeeze=False)
        axes = axes[0]
        names = band_names(m, count, meta)
        if m in RGB_MODALITIES and count >= 3:
            with rasterio.open(tif) as src:
                rgb = src.read(list(RGB_MODALITIES[m])).transpose(1, 2, 0).astype("float32")
            axes = [axes[0]]
            fig, axes = plt.subplots(1, 1, figsize=(5, 5))
            axes.imshow(rgb.astype("uint8"))
            axes.set_title(f"{m} — RGB composite\n{unit}", fontsize=10)
            axes.axis("off")
            panels.append((m, rgb.astype("uint8"), None, unit, small))
            fig.tight_layout()
            fig.savefig(os.path.join(args.out, "per_modality", f"{m}.png"), dpi=95)
            plt.close(fig)
        else:
            for i in range(count):
                a = read_band(tif, i + 1)
                cmap, vmin, vmax = STYLE.get(m, ("viridis", None, None))
                t = f"{m} — {names[i]}"
                im = draw_coarse(axes[i], a, cmap, vmin, vmax, t) if small else \
                    draw_raster(axes[i], a, cmap, vmin, vmax, t)
                fig.colorbar(im, ax=axes[i], fraction=0.046, pad=0.02)
            fig.suptitle(f"{m}  ({unit})" if unit else m, fontsize=12)
            fig.tight_layout()
            fig.savefig(os.path.join(args.out, "per_modality", f"{m}.png"), dpi=95)
            plt.close(fig)
            a0 = read_band(tif, 1)
            panels.append((m, a0, STYLE.get(m, ("viridis", None, None)), unit, small))

        # ---- stats ----
        for i in range(count):
            a = read_band(tif, i + 1)
            fin = np.isfinite(a)
            rows.append({
                "modality": m,
                "band": i + 1,
                "band_name": names[i],
                "unit": unit,
                "shape": f"{a.shape[1]}x{a.shape[0]}",
                "valid_%": round(100 * fin.mean(), 2),
                "min": None if not fin.any() else round(float(np.nanmin(a)), 4),
                "mean": None if not fin.any() else round(float(np.nanmean(a)), 4),
                "max": None if not fin.any() else round(float(np.nanmax(a)), 4),
                "p50": None if not fin.any() else round(float(np.nanmedian(a)), 4),
            })
        print(f"  rendered {m} ({count} band(s))")

    # ---- overview montage ----
    n = len(panels)
    ncol = 6
    nrow = int(np.ceil(n / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(3.0 * ncol, 3.2 * nrow))
    axes = np.atleast_1d(axes).ravel()
    for ax, (m, arr, style, unit, small) in zip(axes, panels):
        if arr.ndim == 3:
            ax.imshow(arr.astype("uint8"))
            ax.set_title(m, fontsize=9)
            ax.axis("off")
        else:
            cmap, vmin, vmax = style
            draw_coarse(ax, arr, cmap, vmin, vmax, m) if small else \
                draw_raster(ax, arr, cmap, vmin, vmax, m)
    for ax in axes[n:]:
        ax.axis("off")
    fig.suptitle(
        f"Singapore · 2KM tile {args.tile} · {args.year} · {n} modalities",
        fontsize=16, y=0.997,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.985])
    fig.savefig(os.path.join(args.out, "overview_montage.png"), dpi=100)
    plt.close(fig)

    # ---- stats csv ----
    with open(os.path.join(args.out, "modality_stats.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"\nDone: {len(panels)} modalities, {len(rows)} bands -> {args.out}")


if __name__ == "__main__":
    main()
