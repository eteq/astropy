import matplotlib.pyplot as plt
from astropy.convolution import MexicanHat2DKernel
mexicanhat_2D_kernel = MexicanHat2DKernel(10)
plt.imshow(mexicanhat_2D_kernel, interpolation='none', origin='lower')
plt.xlabel('x [pixels]')
plt.ylabel('y [pixels]')
plt.colorbar()
plt.show()