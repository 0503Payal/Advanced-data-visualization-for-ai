"""Homework 4 — small multiples across colour schemes, with a colour-vision check."""
import numpy as np, pandas as pd, altair as alt, json, vl_convert as vlc
from vega_datasets import data as vega_data

antibiotics = vega_data.burtin()
SCHEMES = ['greys', 'viridis', 'rainbow', 'yelloworangered']

# --------------------------------------------------------------------------
# The chart: the penicillin-resistance heatmap, repeated once per scheme.
# MIC is a concentration spanning 0.001-1000 ug/ml, so the colour scale stays
# logarithmic - on a linear scale every value but the largest collapses into
# one end of the ramp.
# --------------------------------------------------------------------------
def heatmap(scheme):
    return alt.Chart(antibiotics, title=scheme).mark_rect().encode(
        alt.Y('Bacteria:N',
              sort=alt.EncodingSortField(field='Penicillin', op='max',
                                         order='descending'),
              axis=alt.Axis(orient='right', title=None)),
        alt.Color('Penicillin:Q',
                  scale=alt.Scale(type='log', scheme=scheme, nice=True),
                  legend=alt.Legend(titleOrient='right', tickCount=5),
                  title='Penicillin MIC (μg/ml)'),
        tooltip=['Bacteria:N', alt.Tooltip('Penicillin:Q', title='MIC (μg/ml)'),
                 'Gram_Staining:N'],
    ).properties(width=90, height=300)

small_multiple = alt.hconcat(
    *[heatmap(s) for s in SCHEMES], spacing=58
).resolve_scale(
    # without this the panels share one colour scale and every panel renders
    # in the first scheme
    color='independent'
).properties(
    title=alt.TitleParams(
        text='Penicillin resistance across four colour schemes',
        subtitle=['Identical data and identical log scale; only the colour scheme '
                  'changes. Bacteria are sorted by descending MIC,',
                  'so the most resistant strains are at the top of every panel.'],
        anchor='start', fontSize=17, subtitleColor='gray', subtitleFontSize=12),
).configure_title(anchor='start', offset=5).configure_view(stroke=None)

# --------------------------------------------------------------------------
# Colour-vision check. Rather than eyeballing Coblis, the scheme ramps are
# sampled from the rendered output and run through the Machado et al. (2009)
# dichromacy matrices, then compared in CIELAB.
# --------------------------------------------------------------------------
MACHADO = {
 'Protanopia':   [[0.152286, 1.052583, -0.204868],
                  [0.114503, 0.786281,  0.099216],
                  [-0.003882, -0.048116, 1.051998]],
 'Deuteranopia': [[0.367322, 0.860646, -0.227968],
                  [0.280085, 0.672501,  0.047413],
                  [-0.011820, 0.042940, 0.968881]],
 'Tritanopia':   [[1.255528, -0.076749, -0.178779],
                  [-0.078411, 0.930809,  0.147602],
                  [0.004733,  0.691367,  0.303900]],
}

def srgb_to_linear(c):
    c = c / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)

def linear_to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1/2.4) - 0.055) * 255

def simulate(rgb, kind):
    lin = srgb_to_linear(rgb.astype(float))
    out = lin @ np.array(MACHADO[kind]).T
    return linear_to_srgb(out)

def rgb_to_lab(rgb):
    lin = srgb_to_linear(rgb.astype(float))
    M = np.array([[0.4124, 0.3576, 0.1805],
                  [0.2126, 0.7152, 0.0722],
                  [0.0193, 0.1192, 0.9505]])
    xyz = lin @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16/116)
    return np.stack([116*f[:,1]-16, 500*(f[:,0]-f[:,1]), 200*(f[:,1]-f[:,2])], axis=1)

def ramp_colours(scheme, n=24):
    """Render a strip of n swatches with this scheme and read the true colours back."""
    strip = alt.Chart(pd.DataFrame({'i': range(n)})).mark_rect().encode(
        alt.X('i:O', axis=None),
        alt.Color('i:Q', scale=alt.Scale(scheme=scheme), legend=None),
    ).properties(width=n*10, height=20).configure_view(stroke=None)
    import io
    from PIL import Image
    img = Image.open(io.BytesIO(vlc.vegalite_to_png(json.dumps(strip.to_dict()),
                                                    scale=1))).convert('RGB')
    a = np.array(img); row = a[a.shape[0]//2]
    # sample the centre of each swatch, skipping transparent padding
    xs = np.linspace(0, row.shape[0]-1, n*2+1)[1::2].astype(int)
    return row[xs]

if __name__ == '__main__':
    rows = []
    for s in SCHEMES:
        cols = ramp_colours(s)
        for kind in ['Normal'] + list(MACHADO):
            sim = cols if kind == 'Normal' else simulate(cols, kind)
            lab = rgb_to_lab(sim)
            d = np.linalg.norm(np.diff(lab, axis=0), axis=1)   # step-to-step ΔE
            rows.append({'scheme': s, 'vision': kind,
                         'min_step': d.min(), 'mean_step': d.mean(),
                         'total_range': np.linalg.norm(lab[-1]-lab[0])})
    df = pd.DataFrame(rows)
    df.to_csv('cvd_metrics.csv', index=False)
    print(df.pivot(index='scheme', columns='vision', values='min_step')
            .round(2).to_string())
    print()
    print(df.pivot(index='scheme', columns='vision', values='total_range')
            .round(1).to_string())
    small_multiple.save('solution.html')
    small_multiple.save('preview.png', ppi=150)
    print('\nsaved solution.html, preview.png, cvd_metrics.csv')
