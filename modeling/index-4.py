import numpy as np
import matplotlib.pyplot as plt
from astropy.modeling import models
from astropy.convolution import convolve_models

g1 = models.Gaussian1D(1, -1, 1)
g2 = models.Gaussian1D(1, 1, 1)
g3 = convolve_models(g1, g2)

x = np.linspace(-3, -3, 50)
plt.plot(x, g1(x), 'k-')
plt.plot(x, g2(x), 'k-')
plt.plot(x, g3(x), 'k-')