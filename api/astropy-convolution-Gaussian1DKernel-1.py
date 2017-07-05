import matplotlib.pyplot as plt
from astropy.convolution import Gaussian1DKernel
gauss_1D_kernel = Gaussian1DKernel(10)
plt.plot(gauss_1D_kernel, drawstyle='steps')
plt.xlabel('x [pixels]')
plt.ylabel('value')
plt.show()