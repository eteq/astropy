.. include:: references.txt

.. _astropy-coordinates-representations:

Using and Designing Coordinate Representations
----------------------------------------------

Points in a 3-d vector space can be represented in different ways, such as
cartesian, spherical polar, cylindrical, and so on. These underlie the way
coordinate data in `astropy.coordinates` is represented, as described in the
:ref:`astropy-coordinates-overview`. Below, we describe how one can use them on
their own, as a way to convert between different representations, including
ones not built-in, and to do simple vector arithmetic.

The built-in representation classes are:

* `~astropy.coordinates.CartesianRepresentation`: cartesian
  coordinates ``x``, ``y``, and ``z``
* `~astropy.coordinates.SphericalRepresentation`: spherical
  polar coordinates represented by a longitude (``lon``), a latitude
  (``lat``), and a distance (``distance``). The latitude is a value ranging
  from -90 to 90 degrees.
* `~astropy.coordinates.UnitSphericalRepresentation`:
  spherical polar coordinates on a unit sphere, represented by a longitude
  (``lon``) and latitude (``lat``)
* `~astropy.coordinates.PhysicsSphericalRepresentation`:
  spherical polar coordinates, represented by an inclination (``theta``) and
  azimuthal angle (``phi``), and radius ``r``. The inclination goes from 0 to
  180 degrees, and is related to the latitude in the
  `~astropy.coordinates.SphericalRepresentation` by
  ``theta = 90 deg - lat``.
* `~astropy.coordinates.CylindricalRepresentation`:
  cylindrical polar coordinates, represented by a cylindrical radius
  (``rho``), azimuthal angle (``phi``), and height (``z``).

.. Note::
   For information about using and changing the representation of
   `~astropy.coordinates.SkyCoord` objects, see the
   :ref:`astropy-skycoord-representations` section.

Instantiating and converting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Representation classes are instantiated with `~astropy.units.Quantity`
objects::

    >>> from astropy import units as u
    >>> from astropy.coordinates.representation import CartesianRepresentation
    >>> car = CartesianRepresentation(3 * u.kpc, 5 * u.kpc, 4 * u.kpc)
    >>> car
    <CartesianRepresentation (x, y, z) in kpc
        (3.0, 5.0, 4.0)>

Array `~astropy.units.Quantity` objects can also be passed to
representations. They will have the expected shape, which can be changed using
methods with the same names as those for `~numpy.ndarray`, such as ``reshape``,
``ravel``, etc.::

  >>> x = u.Quantity([[1., 0., 0.], [3., 5., 3.]], u.m)
  >>> y = u.Quantity([[0., 2., 0.], [4., 0., -4.]], u.m)
  >>> z = u.Quantity([[0., 0., 3.], [0., 12., -12.]], u.m)
  >>> car_array = CartesianRepresentation(x, y, z)
  >>> car_array
  <CartesianRepresentation (x, y, z) in m
      [[(1.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 3.0)],
       [(3.0, 4.0, 0.0), (5.0, 0.0, 12.0), (3.0, -4.0, -12.0)]]>
  >>> car_array.shape
  (2, 3)
  >>> car_array.ravel()
  <CartesianRepresentation (x, y, z) in m
      [(1.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 3.0), (3.0, 4.0, 0.0),
       (5.0, 0.0, 12.0), (3.0, -4.0, -12.0)]>

Representations can be converted to other representations using the
``represent_as`` method::

    >>> from astropy.coordinates.representation import SphericalRepresentation, CylindricalRepresentation
    >>> sph = car.represent_as(SphericalRepresentation)
    >>> sph  # doctest: +FLOAT_CMP
    <SphericalRepresentation (lon, lat, distance) in (rad, rad, kpc)
        (1.03037682652, 0.601264216679, 7.07106781187)>
    >>> cyl = car.represent_as(CylindricalRepresentation)
    >>> cyl  # doctest: +FLOAT_CMP
    <CylindricalRepresentation (rho, phi, z) in (kpc, rad, kpc)
        (5.83095189485, 1.03037682652, 4.0)>

All representations can be converted to each other without loss of
information, with the exception of
`~astropy.coordinates.UnitSphericalRepresentation`. This class
is used to store the longitude and latitude of points but does not contain
any distance to the points, and assumes that they are located on a unit and
dimensionless sphere::

    >>> from astropy.coordinates.representation import UnitSphericalRepresentation
    >>> sph_unit = car.represent_as(UnitSphericalRepresentation)
    >>> sph_unit  # doctest: +FLOAT_CMP
    <UnitSphericalRepresentation (lon, lat) in rad
        (1.03037682652, 0.601264216679)>

Converting back to cartesian, the absolute scaling information has been
removed, and the points are still located on a unit sphere:

    >>> sph_unit = car.represent_as(UnitSphericalRepresentation)
    >>> sph_unit.represent_as(CartesianRepresentation) # doctest: +FLOAT_CMP
    <CartesianRepresentation (x, y, z) [dimensionless]
        (0.424264068712, 0.707106781187, 0.565685424949)>


Array values and numpy array method analogs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Array `~astropy.units.Quantity` objects can also be passed to representations,
and such representations can be sliced, reshaped, etc., using the same
methods as are available to `~numpy.ndarray`::

  >>> import numpy as np
  >>> x = np.linspace(0., 5., 6)
  >>> y = np.linspace(10., 15., 6)
  >>> z = np.linspace(20., 25., 6)
  >>> car_array = CartesianRepresentation(x * u.m, y * u.m, z * u.m)
  >>> car_array
  <CartesianRepresentation (x, y, z) in m
      [(0.0, 10.0, 20.0), (1.0, 11.0, 21.0), (2.0, 12.0, 22.0),
       (3.0, 13.0, 23.0), (4.0, 14.0, 24.0), (5.0, 15.0, 25.0)]>
  >>> car_array[2]
  <CartesianRepresentation (x, y, z) in m
      (2.0, 12.0, 22.0)>
  >>> car_array.reshape(3, 2)
  <CartesianRepresentation (x, y, z) in m
      [[(0.0, 10.0, 20.0), (1.0, 11.0, 21.0)],
       [(2.0, 12.0, 22.0), (3.0, 13.0, 23.0)],
       [(4.0, 14.0, 24.0), (5.0, 15.0, 25.0)]]>

.. _astropy-coordinates-create-repr:

Creating your own representations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create your own representation class, your class must inherit from the
``BaseRepresentation`` class.  In addition the following must be defined:

* ``__init__`` method:

  Has a signature like ``__init__(self, comp1, comp2, comp3, copy=True)``
  for inputting the representation component values.

* ``from_cartesian`` class method:

  Takes a `~astropy.coordinates.CartesianRepresentation` object and
  returns an instance of your class.

* ``to_cartesian`` method:

  Returns a `~astropy.coordinates.CartesianRepresentation` object.

* ``attr_classes`` class attribute (``OrderedDict``):

  Defines the initializer class for each component.In most cases this
  class should be derived from `~astropy.units.Quantity`. In particular
  these class initializers must take the value as the first argument and
  accept a ``unit`` keyword which takes a `~astropy.units.Unit`
  initializer or ``None`` to indicate no unit. Also not that the keys of
  this dictionary are treated as the names of the components for this
  representation, with the default ordered given in the order they
  appear as keys.

* ``recommended_units`` dictionary (optional):

  Maps component names to the recommended unit to convert the values of
  that component to.  Can be ``None`` (or missing) to indicate there is
  no preferred unit.  If this dictionary is not defined, no conversion
  of components to particular units will occur.

In pseudo-code, this means that your class will look like::

    class MyRepresentation(BaseRepresentation):

        attr_classes = OrderedDict([('comp1', ComponentClass1),
                                     ('comp2', ComponentClass2),
                                     ('comp3', ComponentClass3)])

        # recommended_units is optional
        recommended_units = {'comp1': u.unit1, 'comp2': u.unit2, 'comp3': u.unit3}

        def __init__(self, ...):
            ...

        @classmethod
        def from_cartesian(self, cartesian):
            ...
            return MyRepresentation(...)

        def to_cartesian(self):
            ...
            return CartesianRepresentation(...)

Once you do this, you will then automatically be able to call
``represent_as`` to convert other representations to/from your representation
class.  Your representation will also be available for use in |skycoord|
and all frame classes.

A representation class may also have a ``_unit_representation`` attribute
(although it is not required). This attribute points to the appropriate
"unit" representation (i.e., a representation that is dimensionless). This is
probably only meaningful for subclasses of
`~astropy.coordinates.SphericalRepresentation`, where it is assumed that it
will be a subclass of `~astropy.coordinates.UnitSphericalRepresentation`.


Vector arithmetic
^^^^^^^^^^^^^^^^^

Representations support basic vector arithmetic, in particular taking the
absolute value (i.e., getting the norm), multiplying with and dividing by
quantities, taking dot and cross products, as well as adding, subtracting,
summing and taking averages of representations, and multiplying with matrices.
These are perhaps best seen from the following examples::

  >>> car_array = CartesianRepresentation([[1., 0., 0.], [3., 5.,  3.]] * u.m,
  ...                                     [[0., 2., 0.], [4., 0., -4.]] * u.m,
  ...                                     [[0., 0., 3.], [0.,12.,-12.]] * u.m)
  >>> car_array
  <CartesianRepresentation (x, y, z) in m
      [[(1.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 3.0)],
       [(3.0, 4.0, 0.0), (5.0, 0.0, 12.0), (3.0, -4.0, -12.0)]]>
  >>> abs(car_array)  # doctest: +FLOAT_CMP
  <Quantity [[  1.,  2.,  3.],
             [  5., 13., 13.]] m>
  >>> car_array / abs(car_array)  # doctest: +FLOAT_CMP
  <CartesianRepresentation (x, y, z) [dimensionless]
      [[(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)],
       [(0.6, 0.8, 0.0), (0.38461538, 0.0, 0.92307692),
        (0.23076923, -0.30769231, -0.92307692)]]>
  >>> (car_array[1] - car_array[0]) / (10. * u.s)  # doctest: +FLOAT_CMP
  <CartesianRepresentation (x, y, z) in m / s
      [(0.2, 0.4, 0.0), (0.5, -0.2, 1.2), (0.3, -0.4, -1.5)]>
  >>> car_array.mean(axis=0)  # doctest: +FLOAT_CMP
  <CartesianRepresentation (x, y, z) in m
      [(2.0, 2.0, 0.0), (2.5, 1.0, 6.0), (1.5, -2.0, -4.5)]>
  >>> car_array.sum()  # doctest: +FLOAT_CMP
  <CartesianRepresentation (x, y, z) in m
      (12.0, 2.0, 3.0)>
      
  >>> unit_x = UnitSphericalRepresentation(0.*u.deg, 0.*u.deg)
  >>> unit_y = UnitSphericalRepresentation(90.*u.deg, 0.*u.deg)
  >>> unit_z = UnitSphericalRepresentation(0.*u.deg, 90.*u.deg)
  >>> car_array.dot(unit_x)  # doctest: +FLOAT_CMP
  <Quantity [[ 1., 0., 0.],
             [ 3., 5., 3.]] m>
  >>> car_array.dot(unit_y)  # doctest: +FLOAT_CMP
  <Quantity [[  6.12323400e-17,  2.00000000e+00,  0.00000000e+00],
             [  4.00000000e+00,  3.06161700e-16, -4.00000000e+00]] m>
  >>> car_array.dot(unit_z)  # doctest: +FLOAT_CMP
  <Quantity [[  6.12323400e-17,  0.00000000e+00,  3.00000000e+00],
             [  1.83697020e-16,  1.20000000e+01, -1.20000000e+01]] m>
  >>> car_array.cross(unit_x)  # doctest: +FLOAT_CMP
  <CartesianRepresentation (x, y, z) in m
      [[(0.0, 0.0, 0.0), (0.0, 0.0, -2.0), (0.0, 3.0, 0.0)],
       [(0.0, 0.0, -4.0), (0.0, 12.0, 0.0), (0.0, -12.0, 4.0)]]>

  >>> from astropy.coordinates.matrix_utilities import rotation_matrix
  >>> rotation = rotation_matrix(90 * u.deg, axis='z')
  >>> rotation  # doctest: +FLOAT_CMP
  array([[  6.12323400e-17,   1.00000000e+00,   0.00000000e+00],
         [ -1.00000000e+00,   6.12323400e-17,   0.00000000e+00],
         [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])
  >>> car_array.transform(rotation)  # doctest: +FLOAT_CMP
  <CartesianRepresentation (x, y, z) in m
      [[(0.0, -1.0, 0.0), (2.0, 0.0, 0.0), (0.0, 0.0, 3.0)],
       [(4.0, -3.0, 0.0), (0.0, -5.0, 12.0), (-4.0, -3.0, -12.0)]]>

Note that all arithmetic except the matrix multiplication works with
non-cartesian representations as well.  For operations other than taking the
absolute value, multiplication, and division, this involves converting the
representations to cartesian internally, and then converting the result back to
the original representation.  Hence, for optimal speed it may be best to work
using cartesian representations.
