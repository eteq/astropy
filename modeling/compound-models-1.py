import numpy as np
from astropy.modeling.models import RedshiftScaleFactor, Gaussian1D

class RedshiftedGaussian(RedshiftScaleFactor | Gaussian1D(1, 0.75, 0.1)):
    """Evaluates a Gaussian with optional redshift applied to the input."""

x = np.linspace(0, 1.2, 100)
g0 = RedshiftedGaussian(z_0=0)

plt.figure(figsize=(8, 5))
plt.plot(x, g0(x), 'g--', label='$z=0$')

for z in (0.2, 0.4, 0.6):
    g = RedshiftedGaussian(z_0=z)
    plt.plot(x, g(x), color=plt.cm.OrRd(z),
             label='$z={0}$'.format(z))

plt.xlabel('Energy')
plt.ylabel('Flux')
plt.legend()