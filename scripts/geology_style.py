"""Reusable Matplotlib style and export helpers for geology-figure."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt


PALETTE = {
    "blue": "#3767A8",
    "mid_blue": "#7F9DC3",
    "pale_blue": "#C7E5F2",
    "yellow": "#FAC97B",
    "orange": "#FB8D5F",
    "red": "#D0574F",
    "charcoal": "#252525",
    "light_gray": "#D8D8D8",
}


def mm_to_in(value_mm: float) -> float:
    return value_mm / 25.4


def apply_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 7,
            "axes.labelsize": 7.5,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "legend.fontsize": 6.5,
            "axes.linewidth": 0.75,
            "lines.linewidth": 1.4,
            "xtick.major.width": 0.7,
            "ytick.major.width": 0.7,
            "xtick.major.size": 3.0,
            "ytick.major.size": 3.0,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "legend.frameon": False,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )


def default_dimensions_mm(rows: int, cols: int, complex_layout: bool = False) -> tuple[float, float]:
    if rows < 1 or cols < 1:
        raise ValueError("rows and cols must be positive integers")
    if cols >= 2:
        width_mm = 180.0
    elif rows >= 2 and complex_layout:
        width_mm = 180.0
    else:
        width_mm = 89.0

    if rows == 1:
        height_mm = 70.0 if cols == 1 else 72.0
    elif complex_layout:
        height_mm = 74.0 * rows + 6.0 * (rows - 1)
    else:
        height_mm = 63.0 * rows + 6.0 * (rows - 1)
    return width_mm, height_mm


def create_layout(
    rows: int,
    cols: int,
    *,
    complex_layout: bool = False,
    width_mm: float | None = None,
    height_mm: float | None = None,
    sharex: bool = False,
    sharey: bool = False,
) -> tuple[mpl.figure.Figure, list[mpl.axes.Axes]]:
    apply_style()
    default_width, default_height = default_dimensions_mm(rows, cols, complex_layout)
    width_mm = default_width if width_mm is None else width_mm
    height_mm = default_height if height_mm is None else height_mm
    fig, axes_array = plt.subplots(
        rows,
        cols,
        figsize=(mm_to_in(width_mm), mm_to_in(height_mm)),
        squeeze=False,
        sharex=sharex,
        sharey=sharey,
    )
    return fig, list(axes_array.ravel())


def style_boxed_axes(ax: mpl.axes.Axes) -> None:
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.75)
        spine.set_color(PALETTE["charcoal"])
    ax.tick_params(colors=PALETTE["charcoal"], pad=3)
    ax.xaxis.label.set_color(PALETTE["charcoal"])
    ax.yaxis.label.set_color(PALETTE["charcoal"])
    ax.grid(False)


def add_panel_labels(axes: Sequence[mpl.axes.Axes], labels: Sequence[str] | None = None) -> None:
    if labels is None:
        labels = [chr(ord("a") + index) for index in range(len(axes))]
    if len(labels) != len(axes):
        raise ValueError("labels must match the number of axes")
    for ax, label in zip(axes, labels):
        offset = mpl.transforms.ScaledTranslation(-9 / 72, 3 / 72, ax.figure.dpi_scale_trans)
        ax.text(
            0,
            1,
            label,
            transform=ax.transAxes + offset,
            ha="left",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color="black",
        )


def set_y_axis_color(ax: mpl.axes.Axes, color: str, side: str) -> None:
    if side not in {"left", "right"}:
        raise ValueError("side must be 'left' or 'right'")
    ax.yaxis.label.set_color(color)
    ax.tick_params(axis="y", colors=color)
    ax.spines[side].set_color(color)
    ax.spines[side].set_linewidth(0.9)


def add_right_axis(
    ax: mpl.axes.Axes,
    *,
    color: str,
    outward_pt: float = 0.0,
) -> mpl.axes.Axes:
    twin = ax.twinx()
    if outward_pt:
        twin.spines["right"].set_position(("outward", outward_pt))
    twin.patch.set_visible(False)
    twin.spines["top"].set_visible(False)
    twin.spines["bottom"].set_visible(False)
    twin.spines["left"].set_visible(False)
    set_y_axis_color(twin, color, "right")
    return twin


def _bbox_points(fig: mpl.figure.Figure, ax: mpl.axes.Axes) -> list[float]:
    width_in, height_in = fig.get_size_inches()
    box = ax.get_position()
    return [
        box.x0 * width_in * 72,
        box.y0 * height_in * 72,
        box.x1 * width_in * 72,
        box.y1 * height_in * 72,
    ]


def audit_panel_alignment(
    fig: mpl.figure.Figure,
    axes: Sequence[mpl.axes.Axes],
    *,
    rows: int,
    cols: int,
    tolerance_pt: float = 1.5,
    json_out: str | Path | None = None,
) -> dict:
    if len(axes) != rows * cols:
        raise ValueError("primary axes count must equal rows * cols")
    fig.canvas.draw()
    boxes = [_bbox_points(fig, ax) for ax in axes]
    failures: list[dict] = []

    def compare(check: str, panel_a: int, panel_b: int, value_a: float, value_b: float) -> None:
        delta = abs(value_a - value_b)
        if delta > tolerance_pt:
            failures.append(
                {
                    "check": check,
                    "panels": [panel_a, panel_b],
                    "delta_pt": round(delta, 4),
                }
            )

    for row in range(rows):
        indices = [row * cols + col for col in range(cols)]
        reference = indices[0]
        ref = boxes[reference]
        for index in indices[1:]:
            box = boxes[index]
            compare("row-bottom", reference, index, ref[1], box[1])
            compare("row-top", reference, index, ref[3], box[3])
            compare("row-height", reference, index, ref[3] - ref[1], box[3] - box[1])
            compare("panel-width", reference, index, ref[2] - ref[0], box[2] - box[0])

    for col in range(cols):
        indices = [row * cols + col for row in range(rows)]
        reference = indices[0]
        ref = boxes[reference]
        for index in indices[1:]:
            box = boxes[index]
            compare("column-left", reference, index, ref[0], box[0])
            compare("column-right", reference, index, ref[2], box[2])
            compare("column-width", reference, index, ref[2] - ref[0], box[2] - box[0])

    report = {
        "schema_version": 1,
        "applicable": len(axes) > 1,
        "verdict": "PASS" if not failures else "FIX BEFORE DELIVERY",
        "tolerance_pt": tolerance_pt,
        "rows": rows,
        "cols": cols,
        "panels": [{"index": index, "bbox_pt": box} for index, box in enumerate(boxes)],
        "failures": failures,
    }
    if json_out is not None:
        path = Path(json_out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if failures:
        raise RuntimeError(f"panel alignment failed: {failures}")
    return report


def save_bundle(
    fig: mpl.figure.Figure,
    output_base: str | Path,
    *,
    primary_axes: Iterable[mpl.axes.Axes] | None = None,
    rows: int = 1,
    cols: int = 1,
) -> dict | None:
    base = Path(output_base)
    base.parent.mkdir(parents=True, exist_ok=True)
    axes = list(primary_axes) if primary_axes is not None else []
    report = None
    if rows * cols > 1:
        report = audit_panel_alignment(
            fig,
            axes,
            rows=rows,
            cols=cols,
            json_out=str(base) + ".alignment.json",
        )
    fig.savefig(str(base) + ".svg")
    fig.savefig(str(base) + ".pdf")
    fig.savefig(str(base) + ".png", dpi=300)
    fig.savefig(str(base) + ".tiff", dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    return report
