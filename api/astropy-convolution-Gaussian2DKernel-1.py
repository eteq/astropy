import matplotlib.pyplot as plt
from astropy.convolution import Gaussian2DKernel
gaussian_2D_kernel = Gaussian2DKernel(10)
plt.imshow(gaussian_2D_kernel, interpolation='none', origin='lower')
plt.xlabel('x [pixels]')
plt.ylabel('y [pixels]')
plt.colorbar()
plt.show()