# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Tests for RGB Images
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os
import tempfile

import numpy as np
from numpy.testing import assert_equal

from ...convolution import convolve, Gaussian2DKernel
from ...tests.helper import pytest
from .. import lupton_rgb

try:
    import matplotlib
    matplotlib.use('TkAgg')
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    import scipy.misc
    scipy.misc.imresize  # just checking if it exists.
    HAVE_SCIPY_MISC = True
except (ImportError, AttributeError):
    HAVE_SCIPY_MISC = False

# Set display=True to get matplotlib imshow windows to help with debugging.
display = False


def display_rgb(rgb, title=None):
    """Display an rgb image using matplotlib (useful for debugging)"""
    import matplotlib.pyplot as plt
    plt.imshow(rgb, interpolation='nearest', origin='lower')
    if title:
        plt.title(title)
    plt.show()
    return plt


def saturate(image, satValue):
    """
    Return image with all points above satValue set to NaN.

    Simulates saturation on an image, so we can test 'replace_saturated_pixels'
    """
    result = image.copy()
    saturated = image > satValue
    result[saturated] = np.nan
    return result


def random_array(dtype, N=100):
    return np.array(np.random.random(10)*100, dtype=dtype)


def test_compute_intensity_1_float():
    image_r = random_array(np.float64)
    intensity = lupton_rgb.compute_intensity(image_r)
    assert image_r.dtype == intensity.dtype
    assert_equal(image_r, intensity)


def test_compute_intensity_1_uint():
    image_r = random_array(np.uint8)
    intensity = lupton_rgb.compute_intensity(image_r)
    assert image_r.dtype == intensity.dtype
    assert_equal(image_r, intensity)


def test_compute_intensity_3_float():
    image_r = random_array(np.float64)
    image_g = random_array(np.float64)
    image_b = random_array(np.float64)
    intensity = lupton_rgb.compute_intensity(image_r, image_g, image_b)
    assert image_r.dtype == intensity.dtype
    assert_equal(intensity, (image_r+image_g+image_b)/3.0)


def test_compute_intensity_3_uint():
    image_r = random_array(np.uint8)
    image_g = random_array(np.uint8)
    image_b = random_array(np.uint8)
    intensity = lupton_rgb.compute_intensity(image_r, image_g, image_b)
    assert image_r.dtype == intensity.dtype
    assert_equal(intensity, (image_r+image_g+image_b)//3)


class TestLuptonRgb(object):
    """A test case for Rgb"""

    np.random.seed(1000)  # so we always get the same images.

    min_, range_, Q = 0, 5, 20  # asinh

    width, height = 85, 75
    images = []

    shape = (width, height)
    image_r = np.zeros(shape)
    image_g = np.zeros(shape)
    image_b = np.zeros(shape)

    # pixel locations, values and colors
    points = [[15, 15], [50, 45], [30, 30], [45, 15]]
    values = [1000, 5500, 600, 20000]
    g_r = [1.0, -1.0, 1.0, 1.0]
    r_i = [2.0, -0.5, 2.5, 1.0]

    # Put pixels in the images.
    for p, v, gr, ri in zip(points, values, g_r, r_i):
        image_r[p[0], p[1]] = v*pow(10, 0.4*ri)
        image_g[p[0], p[1]] = v*pow(10, 0.4*gr)
        image_b[p[0], p[1]] = v

    # convolve the image with a reasonable PSF, and add Gaussian background noise
    def convolve_with_noise(image, psf):
        convolvedImage = convolve(image, psf, boundary='extend', normalize_kernel=True)
        randomImage = np.random.normal(0, 2, image.shape)
        return randomImage + convolvedImage

    psf = Gaussian2DKernel(2.5)
    image_r = convolve_with_noise(image_r, psf)
    image_g = convolve_with_noise(image_g, psf)
    image_b = convolve_with_noise(image_b, psf)

    def tearDown(self):
        for im in self.images:
            del im
        del self.images

    def test_Asinh(self):
        """Test creating an RGB image using an asinh stretch"""
        asinhMap = lupton_rgb.AsinhMapping(self.min_, self.range_, self.Q)
        rgbImage = asinhMap.make_rgb_image(self.image_r, self.image_g, self.image_b)
        if display:
            display_rgb(rgbImage, title=sys._getframe().f_code.co_name)

    def test_AsinhZscale(self):
        """Test creating an RGB image using an asinh stretch estimated using zscale"""

        map = lupton_rgb.AsinhZScaleMapping(self.image_r, self.image_g, self.image_b)
        rgbImage = map.make_rgb_image(self.image_r, self.image_g, self.image_b)
        if display:
            display_rgb(rgbImage, title=sys._getframe().f_code.co_name)

    def test_AsinhZscaleIntensity(self):
        """Test creating an RGB image using an asinh stretch estimated using zscale on the intensity"""

        map = lupton_rgb.AsinhZScaleMapping(self.image_r, self.image_g, self.image_b)
        rgbImage = map.make_rgb_image(self.image_r, self.image_g, self.image_b)
        if display:
            display_rgb(rgbImage, title=sys._getframe().f_code.co_name)

    def test_AsinhZscaleIntensityPedestal(self):
        """Test creating an RGB image using an asinh stretch estimated using zscale on the intensity
        where the images each have a pedestal added"""

        pedestal = [100, 400, -400]
        self.image_r += pedestal[0]
        self.image_g += pedestal[1]
        self.image_b += pedestal[2]

        map = lupton_rgb.AsinhZScaleMapping(self.image_r, self.image_g, self.image_b, pedestal=pedestal)
        rgbImage = map.make_rgb_image(self.image_r, self.image_g, self.image_b)
        if display:
            display_rgb(rgbImage, title=sys._getframe().f_code.co_name)

    def test_AsinhZscaleIntensityBW(self):
        """Test creating a black-and-white image using an asinh stretch estimated
        using zscale on the intensity"""

        rgbImage = lupton_rgb.AsinhZScaleMapping(self.image_r).make_rgb_image()
        if display:
            display_rgb(rgbImage, title=sys._getframe().f_code.co_name)

    @pytest.mark.skipif('not HAS_MATPLOTLIB')
    def test_make_rgb(self):
        """Test the function that does it all"""
        satValue = 1000.0
        with tempfile.NamedTemporaryFile(suffix=".png") as temp:
            red = saturate(self.image_r, satValue)
            green = saturate(self.image_g, satValue)
            blue = saturate(self.image_b, satValue)
            lupton_rgb.make_lupton_rgb(red, green, blue, self.min_, self.range_, self.Q, filename=temp)
            assert os.path.exists(temp.name)

    def test_make_rgb_saturated_fix(self):
        satValue = 1000.0
        # TODO: Cannot test with these options yet, as that part of the code is not implemented.
        with pytest.raises(NotImplementedError):
            red = saturate(self.image_r, satValue)
            green = saturate(self.image_g, satValue)
            blue = saturate(self.image_b, satValue)
            lupton_rgb.make_lupton_rgb(red, green, blue, self.min_, self.range_, self.Q,
                                       saturated_border_width=1, saturated_pixel_value=2000)

    def test_linear(self):
        """Test using a specified linear stretch"""

        rgbImage = lupton_rgb.LinearMapping(-8.45, 13.44).make_rgb_image(self.image_r)
        if display:
            display_rgb(rgbImage, title=sys._getframe().f_code.co_name)

    def test_linear_min_max(self):
        """Test using a min/max linear stretch

        N.b. also checks that an image passed to the ctor is used as the default in make_rgb_image()
        """

        rgbImage = lupton_rgb.LinearMapping(image=self.image_r).make_rgb_image()
        if display:
            display_rgb(rgbImage, title=sys._getframe().f_code.co_name)

    def test_saturated(self):
        """Test interpolating saturated pixels"""
        pytest.skip('replaceSaturatedPixels is not implemented in astropy yet')

        satValue = 1000.0
        self.image_r = saturate(self.image_r, satValue)
        self.image_g = saturate(self.image_g, satValue)
        self.image_b = saturate(self.image_b, satValue)

        lupton_rgb.replaceSaturatedPixels(self.image_r, self.image_g, self.image_b, 1, 2000)
        # Check that we replaced those NaNs with some reasonable value
        assert np.isfinite(self.image_r.getImage().getArray()).all()
        assert np.isfinite(self.image_g.getImage().getArray()).all()
        assert np.isfinite(self.image_b.getImage().getArray()).all()

        # Prepare for generating an output file
        # TBD: FROMAFW
        self.imagesR = self.imagesR.getImage()
        self.imagesR = self.imagesG.getImage()
        self.imagesR = self.imagesB.getImage()

        asinhMap = lupton_rgb.AsinhMapping(self.min_, self.range_, self.Q)
        rgbImage = asinhMap.make_rgb_image(self.image_r, self.image_g, self.image_b)
        if display:
            display_rgb(rgbImage, title=sys._getframe().f_code.co_name)

    @pytest.mark.skipif('not HAVE_SCIPY_MISC', reason="Resizing images requires scipy.misc")
    def test_resize_to_uint(self):
        """Test creating an RGB image of a specified size"""

        x_size = self.image_r.shape[0]/2
        y_size = self.image_r.shape[1]/2
        image_r = np.array(self.image_r, dtype=np.uint16)
        image_g = np.array(self.image_g, dtype=np.uint16)
        image_b = np.array(self.image_b, dtype=np.uint16)
        asinhZ = lupton_rgb.AsinhZScaleMapping(image_r)
        rgbImage = asinhZ.make_rgb_image(image_r, image_g, image_b, x_size=x_size, y_size=y_size)
        if display:
            display_rgb(rgbImage, title=sys._getframe().f_code.co_name)

    def _test_resize(self, x_size=None, y_size=None, frac=None):
        """Test creating an RGB image changing the output """

        map = lupton_rgb.AsinhZScaleMapping(self.image_r)
        rgbImage = map.make_rgb_image(self.image_r, self.image_g, self.image_b,
                                      x_size=x_size, y_size=y_size, rescale=frac)

        # TODO: I'm not positive that I got the width/height values correct:
        # afw and numpy have different conventions!
        h, w, _ = rgbImage.shape
        if x_size is not None:
            assert int(x_size) == w
        if y_size is not None:
            assert int(y_size) == h
        if frac is not None:
            assert int(frac*self.image_r.shape[1]) == w
            assert int(frac*self.image_r.shape[0]) == h

    @pytest.mark.skipif('not HAVE_SCIPY_MISC', reason="Resizing images requires scipy.misc")
    def test_resize_x_size_y_size(self):
        self._test_resize(x_size=self.image_r.shape[0]/2, y_size=self.image_r.shape[1]/2)

    @pytest.mark.skipif('not HAVE_SCIPY_MISC', reason="Resizing images requires scipy.misc")
    def test_resize_twice_x_size(self):
        self._test_resize(x_size=2*self.image_r.shape[0])

    @pytest.mark.skipif('not HAVE_SCIPY_MISC', reason="Resizing images requires scipy.misc")
    def test_resize_half_x_size(self):
        self._test_resize(x_size=self.image_r.shape[0]/2)

    @pytest.mark.skipif('not HAVE_SCIPY_MISC', reason="Resizing images requires scipy.misc")
    def test_resize_half_y_size(self):
        self._test_resize(y_size=self.image_r.shape[0]/2)

    @pytest.mark.skipif('not HAVE_SCIPY_MISC', reason="Resizing images requires scipy.misc")
    def test_resize_frac_half(self):
        self._test_resize(frac=0.5)

    @pytest.mark.skipif('not HAVE_SCIPY_MISC', reason="Resizing images requires scipy.misc")
    def test_resize_frac_twice(self):
        self._test_resize(frac=2)

    @pytest.mark.skipif('not HAS_MATPLOTLIB')
    @pytest.mark.skipif('not HAVE_SCIPY_MISC', reason="Resizing images requires scipy.misc")
    def test_make_rgb_resize(self):
        """Test the function that does it all, including rescaling"""
        lupton_rgb.make_lupton_rgb(self.image_r, self.image_g, self.image_b, x_size=40, y_size=60)

        with tempfile.NamedTemporaryFile(suffix=".png") as temp:
            lupton_rgb.make_lupton_rgb(self.image_r, self.image_g, self.image_b, filename=temp, rescale=0.5)
            assert os.path.exists(temp.name)
