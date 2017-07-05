import numpy as np
from astropy.modeling.models import RedshiftScaleFactor, Gaussian1D, Scale

x = np.linspace(1000, 5000, 1000)
g0 = Gaussian1D(1, 2000, 200)  # No redshift is same as redshift with z=0

plt.figure(figsize=(8, 5))
plt.plot(x, g0(x), 'g--', label='$z=0$')

for z in (0.2, 0.4, 0.6):
    rs = RedshiftScaleFactor(z).inverse  # Redshift in wavelength space
    sc = Scale(1. / (1 + z))  # Rescale the flux to conserve energy
    g = rs | g0 | sc
    plt.plot(x, g(x), color=plt.cm.OrRd(z),
             label='$z={0}$'.format(z))

plt.xlabel('Wavelength')
plt.ylabel('Flux')
plt.legend()