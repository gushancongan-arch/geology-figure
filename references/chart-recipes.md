# Geology chart recipes

Choose the smallest chart family that establishes the intended claim.

## Event time series

Use rainfall bars, reservoir-level lines, displacement curves, velocity curves, pore-pressure ratios, or other event-aligned variables. Keep one shared time basis. Use pale-blue intervals only when an event window has a defined meaning.

- Discovery: forcing in panel `a`, response in panel `b`.
- Mechanism: displacement in panel `a`, velocity or pore pressure in panel `b`.
- Multi-axis: use only when synchronization is the inference; otherwise use stacked panels.

## Group comparisons

- Use grouped bars only for genuine aggregate comparisons with a defined uncertainty interval.
- Prefer raw points plus box/violin summaries when sample size is modest.
- Use horizontal point-range plots for effect estimates and confidence intervals.
- Show paired before-after lines when the replicate unit is matched.

## Depth and spatial profiles

Plot depth increasing downward. Keep the same depth direction and limits across comparable panels. A shaded slip-zone interval is acceptable when independently defined; it must not be inferred merely from the plotted peak.

Typical pairs include pore pressure versus depth and shear strain versus depth, or displacement versus depth and material/interface annotations.

## Spatiotemporal matrices

Use a perceptually ordered sequential map. Show units on both axes and a compact colour bar. Preserve missing regions rather than filling them with zero. Rasterize dense cells when needed, but keep labels and vector annotations editable.

## Relationships and validation

- Scatter plots should retain all observations unless a reported exclusion rule applies.
- Distinguish observed-versus-predicted validation from calibration or training fit.
- A 1:1 reference line is not a fitted regression.
- Report metrics only when their data partition and definition are known.

## Model performance

ROC and precision-recall curves answer different questions; pair them when class imbalance matters. Keep model colours consistent and preserve names such as `XGBoost`, `RF`, and `LR` without blind title casing.

## Multi-panel evidence logic

Each figure should normally support one major claim. Panels must contribute different evidence roles such as forcing, response, mechanism, validation, comparison, robustness, or failure boundary. If removing a panel does not weaken the argument, merge, demote, or remove it.
