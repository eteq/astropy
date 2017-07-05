from astropy import units as u
from astropy.visualization.wcsaxes import SphericalCircle

r = SphericalCircle((266.4 * u.deg, -29.1 * u.deg), 0.15 * u.degree,
                     edgecolor='yellow', facecolor='none',
                     transform=ax.get_transform('fk5'))
ax.add_patch(r)