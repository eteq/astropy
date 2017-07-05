import numpy as np
from astropy.modeling.models import Ellipse2D
from astropy.coordinates import Angle
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
x0, y0 = 25, 25
a, b = 20, 10
theta = Angle(30, 'deg')
e = Ellipse2D(amplitude=100., x_0=x0, y_0=y0, a=a, b=b,
              theta=theta.radian)
y, x = np.mgrid[0:50, 0:50]
fig, ax = plt.subplots(1, 1)
ax.imshow(e(x, y), origin='lower', interpolation='none', cmap='Greys_r')
e2 = mpatches.Ellipse((x0, y0), 2*a, 2*b, theta.degree, edgecolor='red',
                      facecolor='none')
ax.add_patch(e2)
plt.show()