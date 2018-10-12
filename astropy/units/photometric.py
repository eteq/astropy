# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
This package defines magnitude zero points.  By default, they are used to
define corresponding magnitudes, but not enabled as regular physical units.
To enable them, do::

    >>> from astropy.units import magnitude_zero_points
    >>> magnitude_zero_points.enable()  # doctest: +SKIP
"""


import numpy as _numpy
from .core import UnitBase, def_unit

from ..constants import si as _si
from . import cgs, si, astrophys


_ns = globals()

def_unit(['Bol', 'L_bol'], _si.L_bol0, namespace=_ns, prefixes=False,
         doc="Luminosity corresponding to absolute bolometric magnitude zero")
def_unit(['bol', 'f_bol'], _si.L_bol0 / (4 * _numpy.pi * (10.*astrophys.pc)**2),
         namespace=_ns, prefixes=False, doc="Irradiance corresponding to "
         "appparent bolometric magnitude zero")
def_unit(['ABflux'], 3631e-23* cgs.erg * cgs.cm**-2 / si.Hz,
         namespace=_ns, prefixes=False,
         doc="AB magnitude zero flux density.")
def_unit(['STflux'], 3631e-12 * cgs.erg * cgs.cm**-2 / si.AA,
         namespace=_ns, prefixes=False,
         doc="ST magnitude zero flux density.")

###########################################################################
# CLEANUP

del UnitBase
del def_unit
del cgs, si, astrophys

###########################################################################
# DOCSTRING

# This generates a docstring for this module that describes all of the
# standard units defined here.
from ..utils import generate_unit_summary as _generate_unit_summary
if __doc__ is not None:
    __doc__ += _generate_unit_summary(globals())
