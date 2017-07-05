import numpy as np
import matplotlib.pyplot as plt
from astropy.modeling.models import Lorentz1D
from astropy.convolution import convolve, Gaussian1DKernel, Box1DKernel

# Fake Lorentz data including noise
lorentz = Lorentz1D(1, 0, 1)
x = np.linspace(-5, 5, 100)
data_1D = lorentz(x) + 0.1 * (np.random.rand(100) - 0.5)

# Smooth data
gauss_kernel = Gaussian1DKernel(2)
smoothed_data_gauss = convolve(data_1D, gauss_kernel)
box_kernel = Box1DKernel(5)
smoothed_data_box = convolve(data_1D, box_kernel)

# Plot data and smoothed data
plt.plot(x, data_1D, label='Original')
plt.plot(x, smoothed_data_gauss, label='Smoothed with Gaussian1DKernel')
plt.plot(x, smoothed_data_box, label='Smoothed with Box1DKernel')
plt.xlabel('x [a.u.]')
plt.ylabel('amplitude [a.u.]')
plt.xlim(-5, 5)
plt.ylim(-0.1, 1.5)
plt.legend(prop={'size':12})
plt.show()