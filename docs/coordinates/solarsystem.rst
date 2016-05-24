.. include:: references.txt

.. _astropy-coordinates-solarsystem:

Solar System Ephemerides
------------------------

`astropy.coordinates` can calculate the |SkyCoord| of some of the major solar
system objects. By default, it uses approximate orbital elements from `ERFA
<https://github.com/liberfa/erfa>`_ routines, but one can also use more precise
ones using the JPL ephemerides (which are derived from dynamical models).  The
default JPL ephemerides (DE430) provide predictions valid roughly for years
between 1550 and 2650. The file is 115 MB and will need to be downloaded the
first time you use this functionality, but will be cached after that.

.. note::
   To use JPL ephemerides requires that the `jplephem
   <https://pypi.python.org/pypi/jplephem>`_ package is installed. This is
   most easily achieved via ``pip install jplephem``, although whatever
   package management system you use might have it as well.

Three functions are provided; :meth:`~astropy.coordinates.get_body`,
:meth:`~astropy.coordinates.get_moon` and
:meth:`~astropy.coordinates.get_body_barycentric`. The first two functions
return |SkyCoord| objects in the `~astropy.coordinates.GCRS` frame, whilst the
latter returns a `~astropy.coordinates.CartesianRepresentation` of the
barycentric position of a body (i.e in the `~astropy.coordinates.ICRS` frame).

Here are some examples of these functions in use with the ``de432s``
ephemeris (which is a smaller, ~10 MB, file valid between 1950 and 2050)::

  >>> from astropy.time import Time
  >>> from astropy.coordinates import solar_system_ephemeris, EarthLocation
  >>> from astropy.coordinates import get_body_barycentric, get_body, get_moon
  >>> t = Time("2014-09-22 23:22")
  >>> loc = EarthLocation.of_site('greenwich')
  >>> solar_system_ephemeris.set('de432s') # doctest: +REMOTE_DATA, +IGNORE_OUTPUT
  <ScienceState solar_system_ephemeris: 'de432s'>
  >>> get_body('jupiter', t, loc) # doctest: +REMOTE_DATA, +FLOAT_CMP
  <SkyCoord (GCRS: obstime=2014-09-22 23:22:00.000, obsgeoloc=[ 3949481.6898847   -550931.9118969   4961151.73733442] m, obsgeovel=[  40.1745933   288.00078051   -0.        ] m / s): (ra, dec, distance) in (deg, deg, km)
      (136.90234781, 17.03160686, 889196019.15383542)>
  >>> get_moon(t, loc) # doctest: +REMOTE_DATA, +FLOAT_CMP
  <SkyCoord (GCRS: obstime=2014-09-22 23:22:00.000, obsgeoloc=[ 3949481.6898847   -550931.9118969   4961151.73733442] m, obsgeovel=[  40.1745933   288.00078051   -0.        ] m / s): (ra, dec, distance) in (deg, deg, km)
      (165.51840735, 2.32900633, 407226.68749643)>
  >>> get_body_barycentric('moon', t) # doctest: +REMOTE_DATA, +FLOAT_CMP
  <CartesianRepresentation (x, y, z) in km
      (150107535.1073409, -866789.11996916, -418963.55218495)>

For lower precision estimates that do not require downloading an ephemeris::

  >>> solar_system_ephemeris.set('approximate')
  <ScienceState solar_system_ephemeris: 'approximate'>
  >>> get_body('jupiter', t, loc)  # doctest: +FLOAT_CMP
  <SkyCoord (GCRS: obstime=2014-09-22 23:22:00.000, obsgeoloc=[ 3949481.6898847   -550931.9118969   4961151.73733442] m, obsgeovel=[  40.1745933   288.00078051   -0.        ] m / s): (ra, dec, distance) in (deg, deg, AU)
      (136.91116201, 17.02935408, 5.94386022)>

For one-off calculations with a given ephemeris, one can also pass it directly
to the various functions::

  >>> get_body_barycentric('moon', t, ephemeris='de432s')
  ... # doctest: +REMOTE_DATA, +FLOAT_CMP
  <CartesianRepresentation (x, y, z) in km
      (150107535.1073409, -866789.11996916, -418963.55218495)>

For a list of the bodies for which positions can be calculated, do::

  >>> solar_system_ephemeris.bodies
  ('earth',
   'sun',
   'mercury',
   'venus',
   'earth-moon-barycenter',
   'mars',
   'jupiter',
   'saturn',
   'uranus',
   'neptune')
  >>> solar_system_ephemeris.set('de432s') # doctest: +REMOTE_DATA
  <ScienceState solar_system_ephemeris: 'de432s'>
  >>> solar_system_ephemeris.bodies # doctest: +REMOTE_DATA
  ('sun',
   'mercury',
   'venus',
   'earth-moon-barycenter',
   'earth',
   'moon',
   'mars',
   'jupiter',
   'saturn',
   'uranus',
   'neptune',
   'pluto')

.. note ::
    While the sun is included in the these ephemerides, it is important to
    recognize that `~astropy.coordinates.get_sun` does *not* use this
    method, but instead uses a polynomial model for the location of the sun
    (as this requires no special download). So it is not safe to assume that
    ``get_body(time, 'sun')`` and ``get_sun(time)`` will give the same result.
