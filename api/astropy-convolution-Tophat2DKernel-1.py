import matplotlib.pyplot as plt
from astropy.convolution import Tophat2DKernel
tophat_2D_kernel = Tophat2DKernel(40)
plt.imshow(tophat_2D_kernel, interpolation='none', origin='lower')
plt.xlabel('x [pixels]')
plt.ylabel('y [pixels]')
plt.colorbar()
plt.show()