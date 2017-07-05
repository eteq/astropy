import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt
from astropy.stats import sigma_clip, mad_std

# Generate fake data that has a mean of 0 and standard deviation of 0.2 with outliers
np.random.seed(0)
x = np.arange(200)
y = np.zeros(200)
c = stats.bernoulli.rvs(0.35, size=x.shape)
y += (np.random.normal(0., 0.2, x.shape) +
      c*np.random.normal(3.0, 5.0, x.shape))

filtered_data = sigma_clip(y, sigma=3, iters=1, stdfunc=mad_std)

# plot the original and rejected data
plt.figure(figsize=(8,5))
plt.plot(x, y, '+', color='#1f77b4', label="original data")
plt.plot(x[filtered_data.mask], y[filtered_data.mask], 'x',
         color='#d62728', label="rejected data")
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc=2, numpoints=1)