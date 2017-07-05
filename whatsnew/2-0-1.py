import numpy as np
from matplotlib import pyplot as plt
from astropy.stats import RipleysKEstimator
z = np.random.uniform(low=5, high=10, size=(100, 2))
Kest = RipleysKEstimator(area=25, x_max=10, y_max=10, x_min=5, y_min=5)
r = np.linspace(0, 2.5, 100)
plt.plot(r, Kest.poisson(r), label='poisson')
plt.plot(r, Kest(data=z, radii=r, mode='none'), label='none')
plt.plot(r, Kest(data=z, radii=r, mode='translation'), label='translation')
plt.plot(r, Kest(data=z, radii=r, mode='ohser'), label='ohser')
plt.plot(r, Kest(data=z, radii=r, mode='var-width'), label='var-width')
plt.plot(r, Kest(data=z, radii=r, mode='ripley'), label='ripley')
plt.legend(loc='upper left')