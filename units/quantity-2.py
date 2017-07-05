from astropy import units as u
from astropy.visualization import quantity_support
quantity_support()
from matplotlib import pyplot as plt
plt.figure(figsize=(5,3))
plt.plot([1, 2, 3] * u.m)
plt.plot([1, 2, 3] * u.cm)