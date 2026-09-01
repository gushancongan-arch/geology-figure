# Personal style contract

## Matrix notation and dimensions

Interpret layout dimensions as mathematical matrices:

- `1 x 2` means one row and two columns.
- `2 x 1` means two rows and one column.
- In general, use `rows x columns`.

Default final widths:

| Layout | Default width | Use |
|---|---:|---|
| `1 x 1` | 89 mm | ordinary single panel |
| `1 x 2` | 180 mm | horizontal two-panel composite |
| simple `2 x 1` | 89 mm | vertical single-column composite |
| complex `2 x 1` | 180 mm | heatmaps, long labels, dual/triple axes, or dense legends |

The target journal's production dimensions override these defaults.

## Typography

- Font family: Arial, Helvetica, then DejaVu Sans fallback.
- Default body, ticks, and legend: 7 pt; legends may use 6.5 pt when necessary.
- Axis labels: 7.5-8 pt.
- Lowercase bold panel labels: 8.5-9 pt, outside the upper-left plot corner with a fixed point offset.
- Absolute rendered glyph floor: 5 pt.
- Keep variables, symbols, subscripts, superscripts, and units scientifically correct; do not shrink them below the floor.

## Axes and line language

- White figure and axes background.
- Four-sided boxed axes are the default.
- Major ticks point inward; do not show a default grid.
- Default spine width: 0.75 pt.
- Default data-line width: 1.3-1.6 pt.
- Reference lines use light grey and 0.8-1.0 pt; dashed lines are reserved for references, thresholds, or fitted relationships.
- Do not hide relevant baselines or truncate scales merely to enlarge an effect.

## Colour semantics

| Role | Hex | Default meaning |
|---|---|---|
| primary blue | `#3767A8` | baseline, primary neutral series, rainfall |
| secondary blue | `#7F9DC3` | lower response, secondary neutral series |
| pale blue | `#C7E5F2` | forcing window, uncertainty/background interval |
| yellow | `#FAC97B` | intermediate state or restrained highlight |
| orange | `#FB8D5F` | transition, reservoir variation, secondary signal |
| red | `#D0574F` | strongest response, failure, hazard, or decisive evidence |

Red is not an arbitrary category colour. Use it only when the scientific meaning is stronger response, higher hazard, degradation, failure, or decisive evidence. Use grey for pairing lines, neutral references, and secondary structure.

For continuous matrices, use a monotonic sequence derived from pale blue through blue and restrained warm accents. Do not use rainbow, jet, or HSV maps.

## Legends and direct labels

- Place a legend inside the plot only when a genuine empty region exists.
- Move the legend outside when it crosses data, uncertainty, bars, heatmaps, or reference lines.
- Use one shared legend for repeated categories across panels.
- Prefer direct end labels for stable line identities when they remain clear.
- Do not mask a curve with an opaque white text box.
- Do not add a redundant legend when colour-matched axis labels make a dual/triple-axis mapping unambiguous.

## Dual and triple y axes

Dual and triple axes are allowed, not mandatory.

- All y variables must share the same x domain and observation basis.
- Every axis shows a complete variable name and unit.
- The left axis carries the primary forcing or response.
- The first right axis remains at the normal right spine.
- A third y axis is placed on an outward-shifted right spine, normally 36-44 pt.
- Axis label, tick, and spine colour must map one-to-one to the corresponding data series.
- Keep the primary axes four-sided; auxiliary twins should not duplicate top, bottom, or left spines.
- Reserve enough right margin for the outer axis; never solve crowding by shrinking text below the minimum.
- If three axes remain ambiguous or collide at 180 mm width, replace them with stacked panels.

## Formal-figure boundary

Do not add a figure-level title, colour card, colour hex labels, demo banner, institution logo, watermark, or decorative headline to a formal manuscript figure. Put explanations in the caption or manuscript text.
