from astropy.wcs import WCS
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
import matplotlib.pyplot as plt

filename = get_pkg_data_filename('galactic_center/gc_msx_e.fits')

hdu = fits.open(filename)[0]
wcs = WCS(hdu.header)

ax = plt.subplot(projection=wcs)
ax.imshow(hdu.data, vmin=-2.e-5, vmax=2.e-4, origin='lower')