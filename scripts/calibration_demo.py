"""Generate deterministic style-calibration outputs for geology-figure."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import geology_style as gs


def sigmoid(values: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-values))


def event_data() -> dict[str, np.ndarray]:
    day = np.linspace(0, 12, 97)
    rainfall = (
        18 * np.exp(-((day - 2.1) / 0.55) ** 2)
        + 52 * np.exp(-((day - 6.0) / 0.72) ** 2)
        + 27 * np.exp(-((day - 8.0) / 0.60) ** 2)
    )
    reservoir = 174.6 - 0.12 * day - 3.6 * sigmoid((day - 5.3) / 0.75)
    reservoir += 0.55 * sigmoid((day - 10.2) / 0.55)
    upper = 0.45 + 0.03 * day + 8.5 * sigmoid((day - 6.9) / 0.72)
    middle = 0.65 + 0.05 * day + 22.0 * sigmoid((day - 6.7) / 0.62)
    toe = 0.80 + 0.08 * day + 46.0 * sigmoid((day - 6.6) / 0.53)
    velocity = np.gradient(toe, day)
    pore_ratio = 0.14 + 0.70 * sigmoid((day - 6.15) / 0.58)
    pore_ratio += 0.055 * np.exp(-((day - 7.8) / 1.05) ** 2)
    return {
        "event_day": day,
        "rainfall_mm_day": rainfall,
        "reservoir_level_m": reservoir,
        "upper_displacement_mm": upper,
        "middle_displacement_mm": middle,
        "toe_displacement_mm": toe,
        "toe_velocity_mm_day": velocity,
        "pore_pressure_ratio": pore_ratio,
    }


def write_csv(data: dict[str, np.ndarray], path: Path) -> None:
    names = list(data)
    matrix = np.column_stack([data[name] for name in names])
    np.savetxt(path, matrix, delimiter=",", header=",".join(names), comments="", fmt="%.6f")


def vertical_single_column(data: dict[str, np.ndarray], output: Path) -> None:
    fig, axes = gs.create_layout(2, 1, width_mm=89, height_mm=132, sharex=True)
    fig.subplots_adjust(left=0.19, right=0.97, bottom=0.11, top=0.97, hspace=0.17)
    day = data["event_day"]

    axes[0].bar(day, data["rainfall_mm_day"], width=0.105, color=gs.PALETTE["blue"], edgecolor="none")
    axes[0].set(xlim=(0, 12), ylim=(0, 60), ylabel="Rainfall (mm/day)")
    axes[0].set_yticks([0, 20, 40, 60])
    axes[0].tick_params(axis="x", labelbottom=False)

    axes[1].plot(day, data["upper_displacement_mm"], color=gs.PALETTE["mid_blue"], label="Upper slope")
    axes[1].plot(day, data["middle_displacement_mm"], color=gs.PALETTE["blue"], label="Mid-slope")
    axes[1].plot(day, data["toe_displacement_mm"], color=gs.PALETTE["red"], label="Toe")
    axes[1].set(xlim=(0, 12), ylim=(0, 52), xlabel="Event time (day)", ylabel="Cumulative displacement (mm)")
    axes[1].set_xticks([0, 2, 4, 6, 8, 10, 12])
    axes[1].legend(loc="upper left", handlelength=1.7, labelspacing=0.3, borderaxespad=0.5)

    for ax in axes:
        gs.style_boxed_axes(ax)
    gs.add_panel_labels(axes)
    gs.save_bundle(fig, output / "vertical-2x1-89mm", primary_axes=axes, rows=2, cols=1)
    plt.close(fig)


def add_triple_axis(ax: mpl.axes.Axes, data: dict[str, np.ndarray]) -> list[mpl.axes.Axes]:
    day = data["event_day"]
    reservoir_axis = gs.add_right_axis(ax, color=gs.PALETTE["orange"])
    displacement_axis = gs.add_right_axis(ax, color=gs.PALETTE["red"], outward_pt=42)
    ax.bar(day, data["rainfall_mm_day"], width=0.105, color=gs.PALETTE["blue"], alpha=0.78, edgecolor="none")
    reservoir_axis.plot(day, data["reservoir_level_m"], color=gs.PALETTE["orange"])
    displacement_axis.plot(day, data["toe_displacement_mm"], color=gs.PALETTE["red"], linewidth=1.55)
    ax.set(xlim=(0, 12), ylim=(0, 60), ylabel="Rainfall (mm/day)")
    ax.set_yticks([0, 20, 40, 60])
    reservoir_axis.set(ylim=(168.5, 175.5), ylabel="Reservoir level (m)")
    reservoir_axis.set_yticks([169, 171, 173, 175])
    displacement_axis.set(ylim=(0, 55), ylabel="Toe displacement (mm)")
    displacement_axis.set_yticks([0, 10, 20, 30, 40, 50])
    gs.style_boxed_axes(ax)
    gs.set_y_axis_color(ax, gs.PALETTE["blue"], "left")
    return [reservoir_axis, displacement_axis]


def triple_axis(data: dict[str, np.ndarray], output: Path) -> None:
    fig, axes = gs.create_layout(1, 1, width_mm=180, height_mm=76)
    fig.subplots_adjust(left=0.085, right=0.79, bottom=0.19, top=0.96)
    add_triple_axis(axes[0], data)
    axes[0].set_xticks([0, 2, 4, 6, 8, 10, 12])
    axes[0].set_xlabel("Event time (day)")
    gs.save_bundle(fig, output / "triple-axis-180mm", primary_axes=axes, rows=1, cols=1)
    plt.close(fig)


def complex_vertical(data: dict[str, np.ndarray], output: Path) -> None:
    fig, axes = gs.create_layout(2, 1, complex_layout=True, width_mm=180, height_mm=150, sharex=True)
    fig.subplots_adjust(left=0.085, right=0.79, bottom=0.11, top=0.97, hspace=0.17)
    day = data["event_day"]
    add_triple_axis(axes[0], data)
    axes[0].tick_params(axis="x", labelbottom=False)

    pore_axis = gs.add_right_axis(axes[1], color=gs.PALETTE["blue"])
    axes[1].plot(day, data["toe_velocity_mm_day"], color=gs.PALETTE["red"], linewidth=1.5)
    pore_axis.plot(day, data["pore_pressure_ratio"], color=gs.PALETTE["blue"])
    axes[1].set(xlim=(0, 12), ylim=(0, 24), xlabel="Event time (day)", ylabel="Toe velocity (mm/day)")
    axes[1].set_xticks([0, 2, 4, 6, 8, 10, 12])
    axes[1].set_yticks([0, 6, 12, 18, 24])
    pore_axis.set(ylim=(0, 1.0), ylabel="Pore-pressure ratio, rᵤ")
    pore_axis.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    gs.style_boxed_axes(axes[1])
    gs.set_y_axis_color(axes[1], gs.PALETTE["red"], "left")
    gs.add_panel_labels(axes)
    gs.save_bundle(fig, output / "vertical-2x1-complex-180mm", primary_axes=axes, rows=2, cols=1)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("examples/generated"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    data = event_data()
    write_csv(data, args.output / "synthetic-event-data.csv")
    vertical_single_column(data, args.output)
    triple_axis(data, args.output)
    complex_vertical(data, args.output)


if __name__ == "__main__":
    main()
