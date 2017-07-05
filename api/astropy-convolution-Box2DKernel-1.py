import matplotlib.pyplot as plt
from astropy.convolution import Box2DKernel
box_2D_kernel = Box2DKernel(9)
plt.imshow(box_2D_kernel, interpolation='none', origin='lower',
           vmin=0.0, vmax=0.015)
plt.xlim(-1, 9)
plt.ylim(-1, 9)
plt.xlabel('x [pixels]')
plt.ylabel('y [pixels]')
plt.colorbar()
plt.show()