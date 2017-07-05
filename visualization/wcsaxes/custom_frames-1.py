from astropy.wcs import WCS
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
from astropy.visualization.wcsaxes.frame import EllipticalFrame
import matplotlib.pyplot as plt

filename = get_pkg_data_filename('galactic_center/gc_msx_e.fits')
hdu = fits.open(filename)[0]
wcs = WCS(hdu.header)

ax = plt.subplot(projection=wcs, frame_class=EllipticalFrame)

ax.coords.grid(color='white')

im = ax.imshow(hdu.data, vmin=-2.e-5, vmax=2.e-4, origin='lower')

# Clip the image to the frame
im.set_clip_path(ax.coords.frame.patch)