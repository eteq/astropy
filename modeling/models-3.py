import matplotlib.pyplot as plt
import numpy as np
from astropy.modeling import models, fitting
x = np.arange(1, 10, .1)
p1 = models.Polynomial1D(1, n_models=5)
p1.c1 = [0, 1, 2, 3, 4]
y = p1(x, model_set_axis=False)
plt.figure(figsize=(8, 4))
plt.plot(x, y.T)
plt.title("Polynomial1D with a 5 model set on the same input")
plt.show()