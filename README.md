# Interactive Data Visualization in Altair

My work from *Advanced Data Visualization for Artificial Intelligence*
(Freie Universität Berlin). Every chart here is interactive — open the `.html`
files to brush, hover and filter; the `.png` images are static previews.

This repository contains **my solutions only**. Course materials are not
redistributed; each assignment brief is summarised in one line so the work has
context.

## Homework

| # | Task | Result |
|---|---|---|
| 1 | Overview + detail of car production origins over time, with hover and linked brushing | [chart](homework/hw1_overview_and_detail/solution.html) · [write-up](homework/hw1_overview_and_detail) |
| 2 | Population, life expectancy and fertility in three panels on one shared year slider | [chart](homework/hw2_linked_panels/solution.html) · [write-up](homework/hw2_linked_panels) |
| 3 | Diverging vs sequential palette on a 2D histogram | [chart](homework/hw3_diverging_palette/solution.html) · [write-up](homework/hw3_diverging_palette) |
| 4 | Small multiples across four colour schemes, with a colour-vision accessibility check | [chart](homework/hw4_colour_schemes/solution.html) · [notebook](homework/hw4_colour_schemes/solution.ipynb) · [write-up](homework/hw4_colour_schemes) |

### Worth a look: Homework 4

The assignment asks for an accessibility check using an online colour-blindness
simulator. Instead of eyeballing a screenshot, I sampled each colour ramp from
its own rendered output, ran it through the Machado et al. (2009) dichromacy
matrices, and measured the result in CIELAB.

That turned an impression into a finding: **the `rainbow` scheme has a total
perceptual range of 0.0 — for normal vision too.** It is cyclic, beginning and
ending on the same purple, so the most and least antibiotic-resistant bacteria
come out the same colour. It is not an accessibility failure so much as the
wrong scheme for a sequential quantity, for everyone.

`viridis` wins on the numbers: the widest range of the four, 91% of it retained
under deuteranopia, and monotonic ordering preserved under every simulation.

![](homework/hw4_colour_schemes/colour_vision_check.png)

## Exercises

[`exercises/eda_solutions.ipynb`](exercises/eda_solutions.ipynb) — solutions to
the open exercises in the exploratory-data-analysis material, worked on the
sklearn *wine* dataset (178 wines, 13 chemical features, 3 cultivars).

| # | Exercise | Chart |
|---|---|---|
| 1 | Upper triangle of the correlation matrix | [png](exercises/charts/01_correlation_upper_triangle.png) · [html](exercises/charts/01_correlation_upper_triangle.html) |
| 2 | Pairwise mutual information matrix | [png](exercises/charts/02_mutual_information_matrix.png) · [html](exercises/charts/02_mutual_information_matrix.html) |
| 3 | Reordering parallel-coordinates axes | [png](exercises/charts/03_parallel_axis_ordering.png) · [html](exercises/charts/03_parallel_axis_ordering.html) |
| 4 | Min-max normalising instead of standardising | [png](exercises/charts/04_parallel_normalised.png) · [html](exercises/charts/04_parallel_normalised.html) |
| 5 | Hover a line to grey out the other classes | [png](exercises/charts/05_parallel_hover_highlight.png) · [html](exercises/charts/05_parallel_hover_highlight.html) |
| 6 | Min / median / max per variable | [png](exercises/charts/06_parallel_min_median_max.png) · [html](exercises/charts/06_parallel_min_median_max.html) |
| 7 | Linking and brushing on a scatter matrix | [png](exercises/charts/07_scatter_matrix_brushing.png) · [html](exercises/charts/07_scatter_matrix_brushing.html) |
| 8 | Lower triangle only of a scatter matrix | [png](exercises/charts/08_scatter_matrix_lower_triangle.png) · [html](exercises/charts/08_scatter_matrix_lower_triangle.html) |

Three of these needed more than the obvious approach. **Mutual information**
captures non-linear dependence that Pearson correlation misses, but
`mutual_info_score` needs discrete inputs, so each feature is binned first.
**Axis ordering** on a parallel-coordinates chart decides how many lines cross,
so instead of reordering by hand the axes are sorted by an ANOVA-style ratio of
between-class to total variance — the features that separate the cultivars best
end up leftmost. And **the lower triangle** can't be done with `repeat()`, which
always produces a full grid, so it is built explicitly from nested `hconcat`
and `vconcat` with one shared selection across every panel.

## Running it

```bash
pip install -r requirements.txt
jupyter lab
```

All data loads from public URLs (`vega-datasets`) or ships with scikit-learn, so
no data files are needed.

**Stack:** Altair, Vega-Lite, pandas, NumPy, scikit-learn, vl-convert
