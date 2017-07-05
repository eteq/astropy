import numpy as np
import matplotlib.pyplot as plt
import warnings
from astropy.modeling.models import GaussianAbsorption1D
from astropy.utils.exceptions import AstropyDeprecationWarning

plt.figure()
with warnings.catch_warnings():
    warnings.simplefilter('ignore', AstropyDeprecationWarning)
    s1 = GaussianAbsorption1D()
r = np.arange(-5, 5, .01)
for factor in range(1, 4):
    s1.amplitude = factor
    plt.plot(r, s1(r), color=str(0.25 * factor), lw=2)

plt.axis([-5, 5, -3, 2])
plt.show()