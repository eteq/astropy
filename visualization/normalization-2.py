import numpy as np
import matplotlib.pyplot as plt

from astropy.visualization import (MinMaxInterval, SqrtStretch,
                                   ImageNormalize)

# Generate a test image
image = np.arange(65536).reshape((256, 256))

# Create interval object
interval = MinMaxInterval()
vmin, vmax = interval.get_limits(image)

# Create an ImageNormalize object using a SqrtStretch object
norm = ImageNormalize(vmin=vmin, vmax=vmax, stretch=SqrtStretch())

# Display the image
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
im = ax.imshow(image, origin='lower', norm=norm)
fig.colorbar(im)