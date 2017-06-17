.. include:: references.txt

.. _astropy-coordinates-velocities:

Velocity (proper motion and radial) Support
*******************************************

Starting in v2.0, `astropy.coordinates` supports representing velocities and
accounting for them when transforming between coordinate systems.  This includes
full 3D velocities (radial velocities and proper motions), thereby supporting
the tracking of full 6D phase space information in coordinate frame objects.
