# Data integrity and QA

## Source-data boundary

- Preserve the raw input and use all supplied observations by default.
- Never silently drop missing values, outliers, replicates, sites, sensors, dates, or categories.
- Report every exclusion with the exact predicate and before/after counts.
- Do not replace missing observations with zero unless zero is a documented physical observation.
- Generated data are allowed only for installation checks, style calibration, or explicit demonstrations. Keep them in a separate demo output and label them as illustrative.
- A fitted coefficient is not independent validation. Keep fit, conditional extrapolation, external validation, and transportability distinct.

## Uncertainty and statistics

For every aggregate, identify:

- replicate unit and sample size;
- centre statistic;
- SD, SE, confidence interval, quantile interval, or other spread definition;
- statistical test and multiplicity correction, if any;
- exact comparison represented by each annotation.

Use the same uncertainty definition across directly comparable panels or document the exception. For small samples, show raw observations where practical.

## Geometry and alignment

- Measure alignment after the final draw, not from source GridSpec values alone.
- Default tolerance is 1.5 pt for shared edges, plot-area widths/heights, and repeated gutters.
- In `1 x 2`, panels share top and bottom plot-area edges.
- In `2 x 1`, panels share left and right plot-area edges.
- Exclude auxiliary twin axes and inset colour bars from primary-panel comparisons.

## Export bundle

- Editable SVG.
- Editable-text PDF.
- PNG preview, normally 300 dpi.
- TIFF at 600 dpi.
- Plotting source and traceable source data.
- Alignment report for multi-panel figures.

## Final inspection

Inspect each panel and the assembled figure at final physical size:

- no clipping, text-text overlap, or data line crossing through labels;
- panel labels are aligned and legible;
- legends do not obscure evidence;
- axis colours and units are unambiguous, especially for dual/triple axes;
- red remains the visually dominant hazard/decisive signal;
- continuous maps remain interpretable in greyscale and common colour-vision deficiencies;
- no generated data, placeholder labels, or private local paths remain in a production figure.
