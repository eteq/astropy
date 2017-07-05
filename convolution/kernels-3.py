import numpy as np
import matplotlib.pyplot as plt

from astropy.convolution import *
from astropy.modeling.models import Gaussian2D

# Small Gaussian source in the middle of the image
gauss = Gaussian2D(1, 0, 0, 2, 2)
# Fake data including noise
x = np.arange(-100, 101)
y = np.arange(-100, 101)
x, y = np.meshgrid(x, y)
data_2D = gauss(x, y) + 0.1 * (np.random.rand(201, 201) - 0.5)

# Setup kernels, including unity kernel for original image
# Choose normalization for linear scale space for MexicanHat

kernels = [TrapezoidDisk2DKernel(11, slope=0.2),
           Tophat2DKernel(11),
           Gaussian2DKernel(11),
           Box2DKernel(11),
           11 ** 2 * MexicanHat2DKernel(11),
           AiryDisk2DKernel(11)]

fig, axes = plt.subplots(nrows=2, ncols=3)

# Plot kernels
for kernel, ax in zip(kernels, axes.flat):
    smoothed = convolve(data_2D, kernel, normalize_kernel=False)
    im = ax.imshow(smoothed, vmin=-0.01, vmax=0.08, origin='lower',
                   interpolation='None')
    title = kernel.__class__.__name__
    ax.set_title(title, fontsize=12)
    ax.set_yticklabels([])
    ax.set_xticklabels([])

cax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
fig.colorbar(im, cax=cax)
plt.subplots_adjust(left=0.05, right=0.85, top=0.95, bottom=0.05)
plt.show()