import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import make_lupton_rgb
image_r = np.random.random((100,100))
image_g = np.random.random((100,100))
image_b = np.random.random((100,100))
image = make_lupton_rgb(image_r, image_g, image_b, stretch=0.5)
plt.imshow(image)