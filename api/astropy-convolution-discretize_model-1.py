import matplotlib.pyplot as plt
import numpy as np
from astropy.modeling.models import Gaussian1D
from astropy.convolution.utils import discretize_model
gauss_1D = Gaussian1D(1 / (0.5 * np.sqrt(2 * np.pi)), 0, 0.5)
y_center = discretize_model(gauss_1D, (-2, 3), mode='center')
y_corner = discretize_model(gauss_1D, (-2, 3), mode='linear_interp')
y_oversample = discretize_model(gauss_1D, (-2, 3), mode='oversample')
plt.plot(y_center, label='center sum = {0:3f}'.format(y_center.sum()))
plt.plot(y_corner, label='linear_interp sum = {0:3f}'.format(y_corner.sum()))
plt.plot(y_oversample, label='oversample sum = {0:3f}'.format(y_oversample.sum()))
plt.xlabel('pixels')
plt.ylabel('value')
plt.legend()
plt.show()