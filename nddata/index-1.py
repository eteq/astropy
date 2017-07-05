import numpy as np
import matplotlib.pyplot as plt
from astropy.modeling.models import Gaussian2D
y, x = np.mgrid[0:500, 0:600]
data = (Gaussian2D(1, 150, 100, 20, 10, theta=0.5)(x, y) +
        Gaussian2D(0.5, 400, 300, 8, 12, theta=1.2)(x,y) +
        Gaussian2D(0.75, 250, 400, 5, 7, theta=0.23)(x,y) +
        Gaussian2D(0.9, 525, 150, 3, 3)(x,y) +
        Gaussian2D(0.6, 200, 225, 3, 3)(x,y))
np.random.seed(123456)
data += 0.01 * np.random.randn(500, 600)
cosmic_ray_value = 0.997
data[100, 300:310] = cosmic_ray_value
plt.imshow(data, origin='lower')