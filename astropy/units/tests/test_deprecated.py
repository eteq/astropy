# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

# TEST_UNICODE_LITERALS

"""Regression tests for deprecated units or those that are "soft" deprecated
because they are required for VOUnit support but are not in common use."""
from __future__ import (absolute_import, unicode_literals, division,
                        print_function)

from .. import deprecated, prefixed_vounits
from ... import units as u
from ...tests.helper import pytest  # TODO: Stop using bundled pytest


def test_emu():
    with pytest.raises(AttributeError):
        u.emu

    assert u.Bi.to(deprecated.emu, 1) == 1

    with deprecated.enable():
        assert u.Bi.compose()[0] == deprecated.emu

    assert u.Bi.compose()[0] == u.Bi

    # test that the earth/jupiter mass/rad are also in the deprecated bunch
    for body in ('earth', 'jupiter'):
        for phystype in ('Mass', 'Rad'):
            # only test a couple prefixes to same time
            for prefix in ('n', 'y'):
                namewoprefix = body + phystype
                unitname = prefix + namewoprefix

                with pytest.raises(AttributeError):
                    getattr(u, unitname)

                assert (getattr(deprecated, unitname).represents.bases[0] ==
                        getattr(u, namewoprefix))


def test_prefixed_vounits():
    # The tests below could be replicated with all the various prefixes, but it
    # seems unnecessary because they all come as a set.  So we only use nano for
    # the purposes of this test.

    with pytest.raises(AttributeError):
        #nano-solar mass/rad/lum shouldn't be in the base unit namespace
        u.nsolMass
        u.nsolRad
        u.nsolLum

    # but they should be enabled by default via prefixed_vounits, to allow
    # the Unit constructor to accept them
    assert u.Unit('nsolMass') == prefixed_vounits.nsolMass
    assert u.Unit('nsolRad') == prefixed_vounits.nsolRad
    assert u.Unit('nsolLum') == prefixed_vounits.nsolLum

    # but because they are prefixes, they shouldn't be in find_equivalent_units
    assert prefixed_vounits.nsolMass not in u.solMass.find_equivalent_units()
    assert prefixed_vounits.nsolRad not in u.solRad.find_equivalent_units()
    assert prefixed_vounits.nsolLum not in u.solLum.find_equivalent_units()
