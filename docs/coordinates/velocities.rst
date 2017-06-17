.. include:: references.txt

.. _astropy-coordinates-velocities:

Velocity Support (proper motions and radial velocities)
*******************************************************

Starting in v2.0, `astropy.coordinates` supports representing velocities
(through the :ref:`differential <astropy-coordinates-differentials>` objects)
and transforming velocities between astronomical coordinate systems. This
includes support for full 3D velocities (radial velocities and proper motions),
thus enabling encapsulation of full 6D phase space information in coordinate
frame objects.

Proper motion transformations
=============================

Proper motion components specified without a corresponding radial velocity can
be transformed between coordinate frames that only require a spherical rotation.
For example, proper motions are often specified in either the ICRS frame,
:math:`(\mu_\alpha, \mu_\delta)`, or in the Galactic frame, :math:`(\mu_l,
\mu_b)`.

.. Note:: Anywhere a proper motion component is labeled ``pm_*``, the component
   already contains the :math:`\cos({\rm latitude})` term. For example, the
   name ``pm_ra`` is :math:`\mu\cos\delta`.

The transformation from ICRS to Galactic is a pure rotation, so proper
motions can be transformed from one frame to the other::

    >>> icrs = coord.ICRS(ra=132.611*u.deg, dec=11.716*u.deg,
    ...                   pm_ra=-7.508*u.mas/u.yr, pm_dec=0.245*u.mas/u.yr)
    >>> gal = icrs.transform_to(coord.Galactic)
    >>> gal.pm_l, gal.pm_b
    TODO: what exact values?

Radial velocity transformations
===============================

TODO: Erik - maybe fill in an example of doing a "Barycentric correction"?

3D velocity transformations
===========================

When proper motion components and a radial velocity are specified along with a
3D coordinate (sky position and distance), the full-space position and velocity
of the source is fully specified. With 6D information, coordinate objects can be
transformed to a Local Standard of Rest (LSR) frame or a Galactocentric frame in
which the peculiar motion of the Sun or position and full velocity of the Sun
are removed from the coordinate, respectively::

    >>> icrs = coord.ICRS(ra=132.611*u.deg, dec=11.716*u.deg, distance=150*u.pc,
    ...                   pm_ra=-7.508*u.mas/u.yr, pm_dec=0.245*u.mas/u.yr,
    ...                   radial_velocity=-71.324*u.km/u.s)
    >>> icrs.transform_to(coord.LSR)

TODO: explain what values used for peculiar velocity

TODO: Galactocentric::

    >>> icrs = coord.ICRS(ra=132.611*u.deg, dec=11.716*u.deg, distance=150*u.pc,
    ...                   pm_ra=-7.508*u.mas/u.yr, pm_dec=0.245*u.mas/u.yr,
    ...                   radial_velocity=-71.324*u.km/u.s)
    >>> icrs.transform_to(coord.Galactocentric)

TODO: explain how to set Galcen parameters, reference
:ref:`coordinates-galactocentric`
