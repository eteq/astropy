import numpy as np
from scipy.special import erf
from scipy.stats.distributions import binom
import matplotlib.pyplot as plt
from astropy.stats import binned_binom_proportion
def true_efficiency(x):
    return 0.5 - 0.5 * erf((x - 25.) / 2.)
np.random.seed(400)
mag = 20. + 10. * np.random.rand(100)
np.random.seed(600)
detected = binom.rvs(1, true_efficiency(mag))
bins, binshw, p, perr = binned_binom_proportion(mag, detected, bins=20)
plt.errorbar(bins, p, xerr=binshw, yerr=perr, ls='none', marker='o',
             label='estimate')
X = np.linspace(20., 30., 1000)
plt.plot(X, true_efficiency(X), label='true efficiency')
plt.ylim(0., 1.)
plt.title('Detection efficiency vs magnitude')
plt.xlabel('Magnitude')
plt.ylabel('Detection efficiency')
plt.legend()
plt.show()