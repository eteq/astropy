import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import simple_norm

# Generate a test image
image = np.arange(65536).reshape((256, 256))

# Create an ImageNormalize object
norm = simple_norm(image, 'sqrt')

# Display the image
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
im = ax.imshow(image, origin='lower', norm=norm)
fig.colorbar(im)