import numpy as np
from astropy.modeling.models import Rotation2D, Gaussian2D

class RotatedGaussian(Rotation2D | Gaussian2D(1, 0, 0, 0.1, 0.3)):
    """A Gaussian2D composed with a coordinate rotation."""

x, y = np.mgrid[-1:1:0.01, -1:1:0.01]

plt.figure(figsize=(8, 2.5))

for idx, theta in enumerate((0, 45, 90)):
    g = RotatedGaussian(theta)
    plt.subplot(1, 3, idx + 1)
    plt.imshow(g(x, y), origin='lower')
    plt.xticks([])
    plt.yticks([])
    plt.title('Rotated $ {0}^\circ $'.format(theta))