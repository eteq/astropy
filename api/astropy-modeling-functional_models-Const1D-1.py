import numpy as np
import matplotlib.pyplot as plt

from astropy.modeling.models import Const1D

plt.figure()
s1 = Const1D()
r = np.arange(-5, 5, .01)

for factor in range(1, 4):
    s1.amplitude = factor
    plt.plot(r, s1(r), color=str(0.25 * factor), lw=2)

plt.axis([-5, 5, -1, 4])
plt.show()