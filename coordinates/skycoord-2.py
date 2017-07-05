# This is more realistic example how to make a plot in the Aitoff projection
# using data in a SkyCoord object.
# Here a randomly generated data set (multivariate normal distribution)
# for both stars in the bulge and in the disk of a galaxy
# will be used. Both types will be plotted with different number counts. The
# final script can be found below.

# As in the last example, we first import the required packages.
from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
import numpy as np

# We now generate random data for visualisation with
# np.random.multivariate_normal.
disk = np.random.multivariate_normal(mean=[0,0,0], cov=np.diag([1,1,0.5]), size=5000)
bulge = np.random.multivariate_normal(mean=[0,0,0], cov=np.diag([1,1,1]), size=500)
galaxy = np.concatenate([disk, bulge])

# As next step, those coordinates are transformed into an astropy.coordinates
# astropy.coordinates.SkyCoord object.
c_gal = SkyCoord(galaxy, representation='cartesian', frame='galactic')
c_gal_icrs = c_gal.icrs

# Again, as in the last example, we need to convert the coordinates in radians
# and make sure they are between :math:`-\pi` and :math:`\pi`:
ra_rad = c_gal_icrs.ra.wrap_at(180 * u.deg).radian
dec_rad = c_gal_icrs.dec.radian

# We use the same plotting setup as in the last example:
plt.figure(figsize=(8,4.2))
plt.subplot(111, projection="aitoff")
plt.title("Aitoff projection of our random data", y=1.08)
plt.grid(True)
plt.plot(ra_rad, dec_rad, 'o', markersize=2, alpha=0.3)
plt.subplots_adjust(top=0.95,bottom=0.0)
plt.show()