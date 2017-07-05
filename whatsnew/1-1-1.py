import warnings
import numpy as np
from astropy.visualization import hist

# generate some complicated data
rng = np.random.RandomState(0)
t = np.concatenate([-5 + 1.8 * rng.standard_cauchy(500),
                   -4 + 0.8 * rng.standard_cauchy(2000),
                   -1 + 0.3 * rng.standard_cauchy(500),
                   2 + 0.8 * rng.standard_cauchy(1000),
                   4 + 1.5 * rng.standard_cauchy(1000)])

# truncate to a reasonable range
t = t[(t > -15) & (t < 15)]

# draw histograms with two different bin widths
fig = plt.figure(figsize=(10,7))
hist_kwds1 = dict(histtype='stepfilled', alpha=0.2, normed=True)

fig.subplots_adjust(left=0.1, right=0.95, bottom=0.15)
for i, bins in enumerate(['scott', 'freedman', 'knuth', 'blocks']):
    ax = fig.add_subplot(2,2,i+1)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')  # Ignore bayesian block p0 warning
        hist(t, bins=bins, ax=ax, histtype='stepfilled',
             alpha=0.4, normed=True)
    ax.set_xlabel('t')
    ax.set_ylabel('P(t)')
    ax.set_title('hist(t, bins="{0}")'.format(bins),
                 fontdict=dict(family='monospace'), size=14)