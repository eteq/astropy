import numpy as np
from astropy import units as u

x = np.linspace(1, 5, 30) * u.micron
y = np.exp(-0.5 * (x - 2.5 * u.micron)**2 / (200 * u.nm)**2) * u.mJy
plt.plot(x, y, 'ko')
plt.xlabel('Wavelength (microns)')
plt.ylabel('Flux density (mJy)')