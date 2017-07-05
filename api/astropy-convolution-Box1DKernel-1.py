import matplotlib.pyplot as plt
from astropy.convolution import Box1DKernel
box_1D_kernel = Box1DKernel(9)
plt.plot(box_1D_kernel, drawstyle='steps')
plt.xlim(-1, 9)
plt.xlabel('x [pixels]')
plt.ylabel('value')
plt.show()