import matplotlib.pyplot as plt
from astropy.convolution import Moffat2DKernel
moffat_2D_kernel = Moffat2DKernel(3, 2)
plt.imshow(moffat_2D_kernel, interpolation='none', origin='lower')
plt.xlabel('x [pixels]')
plt.ylabel('y [pixels]')
plt.colorbar()
plt.show()