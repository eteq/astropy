import numpy as np
import matplotlib.pyplot as plt
from astropy.modeling.models import Gaussian2D
y, x = np.mgrid[0:500, 0:500]
data = Gaussian2D(1, 50, 100, 10, 5, theta=0.5)(x, y)
plt.imshow(data, origin='lower')