import matplotlib.pyplot as plt
from astropy.convolution import Ring2DKernel
ring_2D_kernel = Ring2DKernel(9, 8)
plt.imshow(ring_2D_kernel, interpolation='none', origin='lower')
plt.xlabel('x [pixels]')
plt.ylabel('y [pixels]')
plt.colorbar()
plt.show()