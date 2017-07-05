import matplotlib.pyplot as plt
from astropy.convolution import MexicanHat1DKernel
mexicanhat_1D_kernel = MexicanHat1DKernel(10)
plt.plot(mexicanhat_1D_kernel, drawstyle='steps')
plt.xlabel('x [pixels]')
plt.ylabel('value')
plt.show()