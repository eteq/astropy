import numpy as np
import matplotlib.pyplot as plt
from astropy.modeling.models import Gaussian2D
from astropy.nddata import Cutout2D
y, x = np.mgrid[0:500, 0:500]
data = Gaussian2D(1, 50, 100, 10, 5, theta=0.5)(x, y)
position = (49.7, 100.1)
size = (40, 50)
cutout = Cutout2D(data, position, size)
plt.imshow(data, origin='lower')
cutout.plot_on_original(color='white')