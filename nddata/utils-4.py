import numpy as np
import matplotlib.pyplot as plt
from astropy.modeling.models import Gaussian2D
from astropy.nddata import Cutout2D
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
y, x = np.mgrid[0:500, 0:500]
data = Gaussian2D(1, 50, 100, 10, 5, theta=0.5)(x, y)
position = SkyCoord('13h11m29.96s -01d19m18.7s', frame='icrs')
wcs = WCS(naxis=2)
rho = np.pi / 3.
scale = 0.05 / 3600.
wcs.wcs.cd = [[scale*np.cos(rho), -scale*np.sin(rho)],
              [scale*np.sin(rho), scale*np.cos(rho)]]
wcs.wcs.ctype = ['RA---TAN', 'DEC--TAN']
wcs.wcs.crval = [position.ra.value, position.dec.value]
wcs.wcs.crpix = [50, 100]
cutout = Cutout2D(data, position, (30, 40), wcs=wcs)
plt.imshow(cutout.data, origin='lower')