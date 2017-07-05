import numpy as np
from astropy.modeling.models import Voigt1D
import matplotlib.pyplot as plt

plt.figure()
x = np.arange(0, 10, 0.01)
v1 = Voigt1D(x_0=5, amplitude_L=10, fwhm_L=0.5, fwhm_G=0.9)
plt.plot(x, v1(x))
plt.show()