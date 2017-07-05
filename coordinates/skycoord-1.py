# This is an example how to make a plot in the Aitoff projection using data
# in a SkyCoord object. Here a randomly generated data set will be used. The
# final script can be found below.

# First we need to import the required packages. We use
# `matplotlib <http://www.matplotlib.org/>`_ here for
# plotting and `numpy <http://www.numpy.org/>`_  to get the value of pi and to
# generate our random data.
from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
import numpy as np

# We now generate random data for visualisation. For RA this is done in the range
# of 0 and 360 degrees (``ra_random``), for DEC between -90 and +90 degrees
# (``dec_random``). Finally, we multiply these values by degrees to get an
# `~astropy.units.Quantity` with units of degrees.
ra_random = np.random.rand(100)*360.0 * u.degree
dec_random = (np.random.rand(100)*180.0-90.0) * u.degree

# As next step, those coordinates are transformed into an astropy.coordinates
# astropy.coordinates.SkyCoord object.
c = SkyCoord(ra=ra_random, dec=dec_random, frame='icrs')

# Because matplotlib needs the coordinates in radians and between :math:`-\pi`
# and :math:`\pi`, not 0 and :math:`2\pi`, we have to convert them.
# For this purpose the `astropy.coordinates.Angle` object provides a special method,
# which we use here to wrap at 180:
ra_rad = c.ra.wrap_at(180 * u.deg).radian
dec_rad = c.dec.radian

# As last step we set up the plotting environment with matplotlib using the
# Aitoff projection with a specific title, a grid, filled circles as markers with
# a markersize of 2 and an alpha value of 0.3.
plt.figure(figsize=(8,4.2))
plt.subplot(111, projection="aitoff")
plt.title("Aitoff projection of our random data", y=1.08)
plt.grid(True)
plt.plot(ra_rad, dec_rad, 'o', markersize=2, alpha=0.3)
plt.subplots_adjust(top=0.95, bottom=0.0)
plt.show()