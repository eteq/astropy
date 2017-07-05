import numpy as np
from astropy.modeling.models import Sersic1D
import matplotlib.pyplot as plt

plt.figure()
plt.subplot(111, xscale='log', yscale='log')
s1 = Sersic1D(amplitude=1, r_eff=5)
r=np.arange(0, 100, .01)

for n in range(1, 10):
     s1.n = n
     plt.plot(r, s1(r), color=str(float(n) / 15))

plt.axis([1e-1, 30, 1e-2, 1e3])
plt.xlabel('log Radius')
plt.ylabel('log Surface Brightness')
plt.text(.25, 1.5, 'n=1')
plt.text(.25, 300, 'n=10')
plt.xticks([])
plt.yticks([])
plt.show()