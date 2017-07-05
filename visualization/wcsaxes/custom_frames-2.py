from astropy.wcs import WCS
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
from astropy.visualization.wcsaxes.frame import EllipticalFrame
from matplotlib import patheffects
import matplotlib.pyplot as plt

filename = get_pkg_data_filename('allsky/allsky_rosat.fits')
hdu = fits.open(filename)[0]
wcs = WCS(hdu.header)

ax = plt.subplot(projection=wcs, frame_class=EllipticalFrame)

path_effects=[patheffects.withStroke(linewidth=3, foreground='black')]
ax.coords.grid(color='white')
ax.coords['glon'].set_ticklabel(color='white', path_effects=path_effects)

im = ax.imshow(hdu.data, vmin=0., vmax=300., origin='lower')

# Clip the image to the frame
im.set_clip_path(ax.coords.frame.patch)