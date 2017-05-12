import numpy as np
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
from astropy.visualization.wcsaxes.frame import EllipticalFrame
from astropy.convolution import Gaussian2DKernel
from scipy.signal import convolve as scipy_convolve
from astropy.convolution import interpolate_replace_nans
import matplotlib.pyplot as plt

# Load the data from data.astropy.org
# Use the same data as above
filename = get_pkg_data_filename('galactic_center/gc_msx_e.fits')
hdu = fits.open(filename)[0]
img = hdu.data[50:90,60:100] * 1e5

# This example is intended to demonstrate how astropy.convolve and
# scipy.convolve handle missing data, so we start by setting the brightest
# pixels to NaN to simulate a "saturated" data set
img[img > 2e1] = np.nan

# We smooth with a Gaussian kernel with stddev=1
# It is a 9x9 array
kernel = Gaussian2DKernel(stddev=1)

# create a "fixed" image with NaNs replaced by interpolated values
fixed_image = interpolate_replace_nans(img, kernel)


# Now we do a bunch of plots.  In the first two plots, the originally masked
# values are marked with red X's
plt.figure(1, figsize=(12,6)).clf()
ax1 = plt.subplot(1,2,1)
im = ax1.imshow(img, vmin=-2., vmax=2.e1, origin='lower',
                interpolation='nearest', cmap='viridis')
y,x = np.where(np.isnan(img))
ax1.set_autoscale_on(False)
ax1.plot(x, y, 'rx', markersize=4)
ax1.set_title("Original")
ax1.set_xticklabels([])
ax1.set_yticklabels([])

ax2 = plt.subplot(1,2,2)
im = ax2.imshow(fixed_image, vmin=-2., vmax=2.e1, origin='lower',
                interpolation='nearest', cmap='viridis')
ax2.set_title("Fixed")
ax2.set_xticklabels([])
ax2.set_yticklabels([])