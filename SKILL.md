---
name: geology-figure
description: Create, revise, and audit publication-grade geology, geotechnical, and landslide figures in Python/Matplotlib using the user's calibrated Origin-inspired style. Use for geological time series, hydro-mechanical dual/triple-axis plots, depth profiles, group comparisons, distributions, heatmaps, validation plots, and labelled multi-panel figures. Do not use for GIS map production, photo editing, or AI-generated mechanism illustrations.
---

# Geology Figure

Create evidence-led scientific figures with a consistent personal visual language. Use Python/Matplotlib for every render and export produced by this skill.

## Before plotting

1. State the one-sentence scientific claim or, for a style test, state that no scientific claim is being made.
2. Map each panel to a distinct evidence role. Do not add panels merely to display another metric.
3. Preserve every supplied observation unless an exclusion is scientifically justified and reported.
4. Use generated data only for an explicitly labelled calibration or demonstration workflow. Never present generated values as measurements.

## Required style contract

Read [references/style-contract.md](references/style-contract.md) before every render. It owns matrix notation, dimensions, typography, boxed axes, colour semantics, legends, and dual/triple-axis rules.

Read [references/chart-recipes.md](references/chart-recipes.md) when choosing a chart family, arranging multi-panel evidence, or using more than one y axis.

Read [references/data-and-qa.md](references/data-and-qa.md) before final export or whenever real data, uncertainty, missing values, filtering, or statistical annotations are involved.

## Reusable implementation

Prefer [scripts/geology_style.py](scripts/geology_style.py) instead of recreating rcParams, dimensions, panel labels, multi-axis styling, alignment checks, and exports.

Use [scripts/calibration_demo.py](scripts/calibration_demo.py) only to verify installation or deliberately generate style-test figures. Its output is demonstrative, not evidence.

## Delivery contract

- Formal figures contain no figure-level title, palette card, demo banner, logo, watermark, or decorative heading unless the user explicitly requests one.
- Export editable SVG and PDF, a PNG preview, and a 600 dpi TIFF.
- Keep every rendered glyph at or above 5 pt; default body text is 7 pt.
- For two or more primary panels, audit final plot-area alignment at a 1.5 pt tolerance.
- Inspect the final PDF/PNG for clipping, label collisions, ambiguous axis mappings, hidden uncertainty, and misleading scales.
- Deliver the plotting source and source data or a traceable data-export file with the figure bundle.
