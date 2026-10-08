# Advanced Data Visualization for AI

Interactive data visualization in [Altair](https://altair-viz.github.io/) /
Vega-Lite — coursework and exercise solutions from the *Advanced Data
Visualization for Artificial Intelligence* course at Freie Universität Berlin
(summer term 2026).

The course works through the grammar of graphics from first principles: marks
and encodings, data transforms, scales and guides, multi-view composition,
interaction, cartography, and text. This repository collects the nine course
notebooks, the submitted homework, and my solutions to the open exercises.

---

## Homework

The assignments set at the end of the course notebooks. Each asks for the result
as a stand-alone interactive HTML page, so that — rather than the notebook — is
the submitted artefact. Open an `.html` file to use the interaction; the `.png`
is a static preview.

| # | Task | Submission |
|---|---|---|
| 1 | Overview + detail of production origins over time, with hover and linked brushing | [html](homework/homework1_overview_and_detail.html) · [png](homework/homework1_overview_and_detail.png) |
| 2 | Population, life expectancy and fertility, three panels linked to a year slider | [html](homework/homework2_gapminder_linked_panels.html) · [png](homework/homework2_gapminder_linked_panels.png) |
| 3 | Diverging colour palette on the 2D histogram | [html](homework/homework3_diverging_colour_histogram.html) · [png](homework/homework3_diverging_colour_histogram.png) |
| 8 | Exploratory analysis of `ori.dat` | pending — dataset not yet available |

**Homework 1** puts a stacked bar chart of models released per region per year
above a horsepower-vs-mileage scatter. An interval selection on the overview
drives the bars' colour through `alt.condition`, so brushing a period highlights
it and greys out the rest; a point selection on the scatter drives both opacity
and size, so hovering a car emphasises it. Both views carry tooltips.

**Homework 2** concatenates three panels — population, life expectancy and
fertility, each against year and coloured by country — and adds one shared
`selection_point` bound to a range slider, so a single control filters all three
at once.

**Homework 3** renders the two-dimensional histogram of Rotten Tomatoes against
IMDB rating twice side by side: once with the PRGn diverging palette, which
makes the transition between low and high counts sharp, and once with sequential
blues plus cell outlines for comparison.

---

## Exercise solutions

[`solutions/09_exploratory_data_analysis_solutions.ipynb`](solutions/09_exploratory_data_analysis_solutions.ipynb)
solves the eight open exercises of the exploratory-data-analysis notebook on
the sklearn *wine* dataset (178 wines, 13 chemical features, 3 cultivars).

| # | Difficulty | Exercise | Chart |
|---|---|---|---|
| 1 | easy | Upper triangle of the correlation matrix | [png](charts/01_correlation_upper_triangle.png) · [html](charts/01_correlation_upper_triangle.html) |
| 2 | medium | Pairwise mutual information matrix | [png](charts/02_mutual_information_matrix.png) · [html](charts/02_mutual_information_matrix.html) |
| 3 | easy | Reordering the parallel-coordinates axes | [png](charts/03_parallel_axis_ordering.png) · [html](charts/03_parallel_axis_ordering.html) |
| 4 | easy | Min-max normalising instead of standardising | [png](charts/04_parallel_normalised.png) · [html](charts/04_parallel_normalised.html) |
| 5 | medium | Hover a line to grey out the other classes | [png](charts/05_parallel_hover_highlight.png) · [html](charts/05_parallel_hover_highlight.html) |
| 6 | hard | Min / median / max per variable | [png](charts/06_parallel_min_median_max.png) · [html](charts/06_parallel_min_median_max.html) |
| 7 | easy | Linking and brushing on the scatter matrix | [png](charts/07_scatter_matrix_brushing.png) · [html](charts/07_scatter_matrix_brushing.html) |
| 8 | hard | Lower triangle only of the scatter matrix | [png](charts/08_scatter_matrix_lower_triangle.png) · [html](charts/08_scatter_matrix_lower_triangle.html) |

The `.png` files are static previews; the `.html` files are the live charts —
download and open one to use the hover highlighting (5) and the linked
brushing (7, 8). A few of the solutions are worth calling out:

**Mutual information (2).** Pearson correlation only sees linear dependence.
Mutual information sees any dependence, but `sklearn.metrics.mutual_info_score`
needs discrete inputs, so each continuous feature is binned into 10 equal-width
bins first. The diagonal is each feature's own entropy.

**Axis ordering (3).** Axis order decides how many lines cross in a parallel
coordinates chart. Instead of reordering by hand, the axes are sorted by an
ANOVA-style ratio — between-class variance over total variance — so the
features that separate the three cultivars best are leftmost and the class
bands become visible immediately.

**Lower triangle (8).** Altair's `repeat()` always produces a full grid and
gives no way to skip cells, so the triangle is built explicitly: one `hconcat`
per row holding only the cells at or left of the diagonal, stacked with
`vconcat`. A single `selection_interval` with `resolve='global'` is shared
across every panel, which is what makes the brushing linked.

---

## Course notebooks

| Notebook | Topic |
|---|---|
| [01](notebooks/01_introduction.ipynb) | Introduction to Altair and Vega-Lite |
| [02](notebooks/02_marks_and_encoding.ipynb) | Marks and encoding channels |
| [03](notebooks/03_data_transformation.ipynb) | Data transformation (aggregate, bin, window) |
| [04](notebooks/04_scales_axes_legends.ipynb) | Scales, axes and legends |
| [05](notebooks/05_view_composition.ipynb) | Multi-view composition |
| [06](notebooks/06_interaction.ipynb) | Selections and interaction |
| [07](notebooks/07_cartographic.ipynb) | Cartographic visualization |
| [08](notebooks/08_textual_analysis.ipynb) | Textual analysis |
| [09](notebooks/09_exploratory_data_analysis.ipynb) | Exploratory data analysis |

All datasets are loaded from public URLs (`vega-datasets`, Project Gutenberg)
or ship with scikit-learn, so no data files are needed to run the notebooks.

---

## Running it

```bash
pip install -r requirements.txt
jupyter lab
```

Charts can be re-exported to `charts/` from the solutions notebook with
`chart.save("name.html")` and `chart.save("name.png", ppi=150)`; PNG export
needs `vl-convert-python`.

---

## Attribution

The notebooks in `notebooks/` are course material from *Advanced Data
Visualization for Artificial Intelligence* at Freie Universität Berlin, with my worked answers
filled in; they are reproduced here for coursework documentation. Parts of the
material derive in turn from the [UW Interactive Data Lab](https://idl.cs.washington.edu/)
Altair curriculum. The homework submissions in `homework/`, the solutions in `solutions/` and the
exported charts are my own work, released under the MIT licence.
