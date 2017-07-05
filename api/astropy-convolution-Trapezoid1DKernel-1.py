import matplotlib.pyplot as plt
from astropy.convolution import Trapezoid1DKernel
trapezoid_1D_kernel = Trapezoid1DKernel(17, slope=0.2)
plt.plot(trapezoid_1D_kernel, drawstyle='steps')
plt.xlabel('x [pixels]')
plt.ylabel('amplitude')
plt.xlim(-1, 28)
plt.show()