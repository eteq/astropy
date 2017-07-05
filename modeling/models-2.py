import matplotlib.pyplot as plt
import numpy as np
from astropy.modeling import models, fitting
x = np.arange(1, 10, .1)
g1 = models.Gaussian1D(amplitude=[10, 9], mean=[2,3], stddev=[.15,.1],
                       n_models=2)
y = g1([x, x - 3])
plt.figure(figsize=(8, 4))
plt.plot(x, y[0])
plt.plot(x - 3, y[1])
plt.title('Evaluate two Gaussian1D models with 2 sets of input data')
plt.show()