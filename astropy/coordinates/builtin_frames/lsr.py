# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import (absolute_import, unicode_literals, division,
                        print_function)

import numpy as np

from .icrs import ICRS
from .galactic import Galactic
from ..baseframe import (QuantityFrameAttribute, TimeFrameAttribute,
                         frame_transform_graph)
from ..transformations import FunctionTransform
from ..representation import CartesianRepresentation
from ... import units as u
from ...time import Time

# TODO: we might want to split this into KinematicLSR and DynamicalLSR (or other
#       words) where 'Kinematic' just has values for the Sun's peculiar motion
#       from, e.g., nearby stars with no consideration of the Galactocentric
#       frame (can could therefore be biased). 'Dynamical' could be tied to
#       parameters in the Galactocentric frame (e.g., circular velocity) so
#       could include values like Bovy+2015's V_tan measurement of 24 km/s.

# For speed
J2000 = Time('J2000')

# TODO: we had to just copy the values because this won't execute properly when
#   the frame transform graph doesn't exist
# _v_ss_icrs = (Galactic(CartesianRepresentation([-11.1, 12.24, 7.25] * u.km/u.s))
#               .transform_to(ICRS).cartesian)

class LSR(ICRS):

    # TODO: these names suck
    # - This is the velocity of the Solar System's barycenter (ICRS) frame
    #   relative to the LSR. Sometimes called the Solar System peculiar
    #   velocity. Here we use the values from [Schönrich et al. 2010]:
    #   [-11.1, 12.24, 7.25] km/s (in the Galactic frame) and rotated into the
    #   ICRS frame (see _v_ss_icrs above)
    # vx_ss_bary = QuantityFrameAttribute(default=_v_ss_icrs[0])
    # vy_ss_bary = QuantityFrameAttribute(default=_v_ss_icrs[1])
    # vz_ss_bary = QuantityFrameAttribute(default=_v_ss_icrs[2])
    vx_ss_bary = QuantityFrameAttribute(default=0.36643981*u.km/u.s)
    vy_ss_bary = QuantityFrameAttribute(default=2.81438204*u.km/u.s)
    vz_ss_bary = QuantityFrameAttribute(default=17.8195139*u.km/u.s)

    obstime = TimeFrameAttribute(default=J2000)


@frame_transform_graph.transform(FunctionTransform, ICRS, LSR)
def icrs_to_lsr(icrs_coord, lsr_frame):
    dt = lsr_frame.obstime - J2000
    vbary = CartesianRepresentation(x=lsr_frame.vx_ss_bary,
                                    y=lsr_frame.vy_ss_bary,
                                    z=lsr_frame.vz_ss_bary)
    new_rep = icrs_coord.cartesian + vbary * dt # TODO: figure out the sign

    return lsr_frame.realize_frame(new_rep)

@frame_transform_graph.transform(FunctionTransform, LSR, ICRS)
def lsr_to_icrs(lsr_coord, icrs_frame):
    dt = lsr_coord.obstime - J2000
    vbary = CartesianRepresentation(x=lsr_coord.vx_ss_bary,
                                    y=lsr_coord.vy_ss_bary,
                                    z=lsr_coord.vz_ss_bary)
    new_rep = lsr_coord.cartesian - vbary * dt # TODO: figure out the sign

    return icrs_frame.realize_frame(new_rep)
