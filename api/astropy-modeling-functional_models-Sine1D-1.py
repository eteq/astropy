import numpy as np
import matplotlib.pyplot as plt

from astropy.modeling.models import Sine1D

plt.figure()
s1 = Sine1D(amplitude=1, frequency=.25)
r=np.arange(0, 10, .01)

for amplitude in range(1,4):
     s1.amplitude = amplitude
     plt.plot(r, s1(r), color=str(0.25 * amplitude), lw=2)

plt.axis([0, 10, -5, 5])
plt.show()