# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
This module contains functions/values used repeatedly in different modules of
the ``builtin_frames`` package.
"""
from __future__ import (absolute_import, unicode_literals, division,
                        print_function)

import warnings

import numpy as np

from ... import units as u
from ... import _erfa as erfa
from ...time import Time
from ...utils import iers
from ...utils.exceptions import AstropyWarning
from ..representation import CartesianRepresentation

# The UTC time scale is not properly defined prior to 1960, so Time('B1950',
# scale='utc') will emit a warning. Instead, we use Time('B1950', scale='tai')
# which is equivalent, but does not emit a warning.
EQUINOX_J2000 = Time('J2000', scale='utc')
EQUINOX_B1950 = Time('B1950', scale='tai')

# This is a time object that is the default "obstime" when such an attribute is
# necessary.  Currently, we use J2000.
DEFAULT_OBSTIME = Time('J2000', scale='utc')

PIOVER2 = np.pi / 2.

# comes from the mean of the 1962-2014 IERS B data
_DEFAULT_PM = (0.035, 0.29)*u.arcsec


def cartrepr_from_matmul(pmat, coo, transpose=False):
    """
    Note that pmat should be an ndarray, *not* a matrix.
    """
    if pmat.shape[-2:] != (3, 3):
        raise ValueError("tried to do matrix multiplication with an array that "
                         "doesn't end in 3x3")
    if coo.isscalar and pmat.shape == (3, 3):
        # a simpler path for scalar coordinates
        if transpose:
            pmat = pmat.T
        newxyz = np.sum(pmat * coo.cartesian.xyz, axis=-1)
    else:
        xyz = coo.cartesian.xyz.T
        # these expression are the same as iterating over the first dimension of
        # pmat and xyz and doing matrix multiplication on each in turn.  resulting
        # dimension is <coo shape> x 3
        pmat = pmat.reshape(pmat.size//9, 3, 3)
        if transpose:
            pmat = pmat.transpose(0, 2, 1)
        newxyz = np.sum(pmat * xyz.reshape(xyz.size//3, 1, 3), axis=-1).T

    return CartesianRepresentation(newxyz)


def get_polar_motion(time):
    """
    gets the two polar motion components in radians for use with apio13
    """
    # Get the polar motion from the IERS table
    xp, yp, status = iers.IERS_Auto.open().pm_xy(time, return_status=True)

    wmsg = None
    if np.any(status == iers.TIME_BEFORE_IERS_RANGE):
        wmsg = ('Tried to get polar motions for times before IERS data is '
                'valid. Defaulting to polar motion from the 50-yr mean for those. '
                'This may affect precision at the 10s of arcsec level')
        xp.ravel()[status.ravel() == iers.TIME_BEFORE_IERS_RANGE] = _DEFAULT_PM[0]
        yp.ravel()[status.ravel() == iers.TIME_BEFORE_IERS_RANGE] = _DEFAULT_PM[1]

        warnings.warn(wmsg, AstropyWarning)

    if np.any(status == iers.TIME_BEYOND_IERS_RANGE):
        wmsg = ('Tried to get polar motions for times after IERS data is '
                'valid. Defaulting to polar motion from the 50-yr mean for those. '
                'This may affect precision at the 10s of arcsec level')

        xp.ravel()[status.ravel() == iers.TIME_BEYOND_IERS_RANGE] = _DEFAULT_PM[0]
        yp.ravel()[status.ravel() == iers.TIME_BEYOND_IERS_RANGE] = _DEFAULT_PM[1]

        warnings.warn(wmsg, AstropyWarning)

    return xp.to(u.radian).value, yp.to(u.radian).value


def _warn_iers(ierserr):
    """
    Generate a warning for an IERSRangeerror

    Parameters
    ----------
    ierserr : An `~astropy.utils.iers.IERSRangeError`
    """
    msg = '{0} Assuming UT1-UTC=0 for coordinate transformations.'
    warnings.warn(msg.format(ierserr.args[0]), AstropyWarning)


def get_dut1utc(time):
    """
    This function is used to get UT1-UTC in coordinates because normally it
    gives an error outside the IERS range, but in coordinates we want to allow
    it to go through but with a warning.
    """
    try:
        return time.delta_ut1_utc
    except iers.IERSRangeError as e:
        _warn_iers(e)
        return np.zeros(time.shape)


def get_jd12(time, scale):
    """
    Gets ``jd1`` and ``jd2`` from a time object in a particular scale.

    Parameters
    ----------
    time : `~astropy.time.Time`
        The time to get the jds for
    scale : str
        The time scale to get the jds for

    Returns
    -------
    jd1 : float
    jd2 : float
    """
    if time.scale == scale:
        newtime = time
    else:
        try:
            newtime = getattr(time, scale)
        except iers.IERSRangeError as e:
            _warn_iers(e)
            newtime = time

    return newtime.jd1, newtime.jd2


def rxp(rmat, p, transpose=True):
    """
    Multiply a p-vector by (the transpose of) an r matrix.

    Parameters
    ----------
    rmat : `~numpy.ndarray`
        rotation matrix
    p : `~numpy.ndarray`
        position vector

    Returns
    --------
    rp : `~numpy.ndarray`
    """
    if rmat.shape[-2:] != (3, 3):
        raise ValueError("tried to do matrix multiplication with an array that "
                         "doesn't end in 3x3")

    if p.ndim == 1 and rmat.shape == (3, 3):
        # a simpler path for scalar coordinates
        if transpose:
            rmat = rmat.T
        result = np.sum(rmat * p, axis=-1).T
    else:
        # these expression are the same as iterating over the first dimension of
        # pmat and xyz and doing matrix multiplication on each in turn.
        rmat = rmat.reshape(rmat.size//9, 3, 3)
        if transpose:
            rmat = rmat.transpose(0, 2, 1)
        result = np.sum(rmat * p.reshape(p.size//3, 1, 3), axis=-1)
    return result


def norm(p):
    """
    Normalise a p-vector.
    """
    return p/np.sqrt(np.sum(p*p, axis=-1, keepdims=True))


def aticq(ri, di, astrom):
    """
    A slightly modified version of the ERFA function ``eraAticq``.

    ``eraAticq`` performs the transformations between two coordinate systems,
    with the details of the transformation being encoded into the ``astrom`` array.

    The companion function ``eraAtciqz`` is meant to be its inverse. However, this
    is not true for directions close to the Solar centre, since the light deflection
    calculations are numerically unstable and therefore not reversible.

    This version sidesteps that problem by artificially reducing the light deflection
    for directions which are within 90 arcseconds of the Sun's position. This is the
    same approach used by the ERFA functions above, except that they use a threshold of
    9 arcseconds.

    Parameters
    ----------
    ri : float or `~numpy.ndarray`
        right ascension, radians
    di : float or `~numpy.ndarray`
        declination, radians
    astrom : eraASTROM array
        ERFA astrometry context, as produced by, e.g. ``eraApci13`` or ``eraApcs13``

    Returns
    --------
    rc : float or `~numpy.ndarray`
    dc : float or `~numpy.ndarray`
    """
    # RA, Dec to cartesian unit vectors
    pos = erfa.s2c(ri, di)

    # Bias-precession-nutation, giving GCRS proper direction.
    ppr = rxp(astrom['bpn'], pos, transpose=True)

    # Aberration, giving GCRS natural direction
    d = np.zeros_like(ppr)
    for j in range(2):
        before = norm(ppr-d)
        after = erfa.ab(before, astrom['v'], astrom['em'], astrom['bm1'])
        d = after - before
    pnat = norm(ppr-d)

    # Light deflection by the Sun, giving BCRS coordinate direction
    d = np.zeros_like(pnat)
    for j in range(5):
        before = norm(pnat-d)
        after = erfa.ld(1.0, before, before, astrom['eh'], astrom['em'], 5e-8)
        d = after - before
    pco = norm(pnat-d)

    # ICRS astrometric RA, Dec
    rc, dc = erfa.c2s(pco)
    return erfa.anp(rc), dc


def atciqz(rc, dc, astrom):
    """
    A slightly modified version of the ERFA function ``eraAtciqz``.

    ``eraAtciqz`` performs the transformations between two coordinate systems,
    with the details of the transformation being encoded into the ``astrom`` array.

    The companion function ``eraAticq`` is meant to be its inverse. However, this
    is not true for directions close to the Solar centre, since the light deflection
    calculations are numerically unstable and therefore not reversible.

    This version sidesteps that problem by artificially reducing the light deflection
    for directions which are within 90 arcseconds of the Sun's position. This is the
    same approach used by the ERFA functions above, except that they use a threshold of
    9 arcseconds.

    Parameters
    ----------
    rc : float or `~numpy.ndarray`
        right ascension, radians
    dc : float or `~numpy.ndarray`
        declination, radians
    astrom : eraASTROM array
        ERFA astrometry context, as produced by, e.g. ``eraApci13`` or ``eraApcs13``

    Returns
    --------
    ri : float or `~numpy.ndarray`
    di : float or `~numpy.ndarray`
    """
    # BCRS coordinate direction (unit vector).
    pco = erfa.s2c(rc, dc)

    # Light deflection by the Sun, giving BCRS natural direction.
    pnat = erfa.ld(1.0, pco, pco, astrom['eh'], astrom['em'], 5e-8)

    # Aberration, giving GCRS proper direction.
    ppr = erfa.ab(pnat, astrom['v'], astrom['em'], astrom['bm1'])

    # Bias-precession-nutation, giving CIRS proper direction.
    # Has no effect if matrix is identity matrix, in which case gives GCRS ppr.
    pi = rxp(astrom['bpn'], ppr, transpose=False)

    # CIRS (GCRS) RA, Dec
    ri, di = erfa.c2s(pi)
    return erfa.anp(ri), di
