# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
This module defines magnitude zero points and related photometric quantities.
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
def_unit(['ABflux'], 10.**(48.6/-2.5) * cgs.erg * cgs.cm**-2 / si.s / si.Hz,
         namespace=_ns, prefixes=False,
         doc="AB magnitude zero flux density.")
def_unit(['STflux'], 10.**(21.1/-2.5) * cgs.erg * cgs.cm**-2 / si.s / si.AA,
         namespace=_ns, prefixes=False,
         doc="ST magnitude zero flux density.")

def_unit(['maggy', 'mgy'],
         namespace=_ns, prefixes=False,
         doc="Maggies - a linear flux unit that is the flux for a mag=0 object."
             "To tie this onto a specific calibrated unit system, the "
             "phot_zero_point equivalency should be used.")
def_unit(['nanomaggy', 'nmgy'], 1e-9 * maggy,
         namespace=_ns, prefixes=False,
         doc="Nanomaggy, i.e. ABmag=22.5")


def phot_zero_point(flux0=1.0*ABflux):
    """
    An equivalency for converting linear flux units ("maggys") defined relative
    to a standard source into a standardized system.

    Parameters
    ----------
    flux0 : u.Quantity
        The flux of a magnitude-0 object in the "maggy" system. Default
        corresponds to a perfect AB-like magnitude system.
    """
    from .quantity import Quantity

    qflux0 = Quantity(flux0, copy=False)

    return [(maggy, qflux0.unit,
             lambda mgy: qflux0.value*mgy,
             lambda flx: flx/qflux0.value)]


###########################################################################
# CLEANUP

del UnitBase
del def_unit
del cgs, si, astrophys

###########################################################################
# DOCSTRING

# This generates a docstring for this module that describes all of the
# standard units defined here.
from .utils import generate_unit_summary as _generate_unit_summary
if __doc__ is not None:
    __doc__ += _generate_unit_summary(globals())
