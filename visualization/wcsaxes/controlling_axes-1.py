from astropy.wcs import WCS
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename

filename = get_pkg_data_filename('l1448/l1448_13co.fits')
hdu = fits.open(filename)[0]
wcs = WCS(hdu.header)

import matplotlib.pyplot as plt

ax = plt.subplot(projection=wcs, slices=(50, 'y', 'x'))
ax.imshow(hdu.data[:, :, 50].transpose())