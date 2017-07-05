import matplotlib.pyplot as plt
from astropy.convolution import TrapezoidDisk2DKernel
trapezoid_2D_kernel = TrapezoidDisk2DKernel(20, slope=0.2)
plt.imshow(trapezoid_2D_kernel, interpolation='none', origin='lower')
plt.xlabel('x [pixels]')
plt.ylabel('y [pixels]')
plt.colorbar()
plt.show()