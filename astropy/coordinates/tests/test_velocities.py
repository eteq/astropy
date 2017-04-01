# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
from ... import units as u
from ...tests.helper import pytest, quantity_allclose
from ..builtin_frames import LSR, ICRS
from ..builtin_frames.lsr import J2000
from ..representation import SphericalDifferential

def test_icrs_lsr():
    """"""

    dt = 1*u.s
    icrs = ICRS(ra=153.612 * u.deg, dec=-11.625 * u.deg,
                distance=1. * u.au)
    lsr = icrs.transform_to(LSR(obstime=J2000 + dt))

    dv = (lsr.cartesian - icrs.cartesian) / dt
    assert quantity_allclose(dv.x, lsr.vx_ss_bary)
    assert quantity_allclose(dv.y, lsr.vy_ss_bary)
    assert quantity_allclose(dv.z, lsr.vz_ss_bary)

    # roundtrip test
    icrs2 = lsr.transform_to(ICRS)
    assert quantity_allclose(icrs.cartesian.xyz, icrs2.cartesian.xyz)

def test_icrs_lsr_differential():

    sph_diff = SphericalDifferential(d_lon=0*u.mas/u.yr, d_lat=0*u.mas/u.yr,
                                     d_distance=0*u.km/u.s)

    icrs = ICRS(ra=153.612 * u.deg, dec=-11.625 * u.deg,
                distance=1. * u.au, differential=sph_diff)
    lsr = icrs.transform_to(LSR)

    assert quantity_allclose(lsr.cartesian.x, lsr.vx_ss_bary)
    assert quantity_allclose(lsr.cartesian.y, lsr.vy_ss_bary)
    assert quantity_allclose(lsr.cartesian.z, lsr.vz_ss_bary)

