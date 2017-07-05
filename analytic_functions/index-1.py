import matplotlib.pyplot as plt
import numpy as np
import warnings
from astropy import constants as const
from astropy import units as u
from astropy.analytic_functions import blackbody_lambda
from astropy.utils.exceptions import AstropyDeprecationWarning

temperature = 5000 * u.K
wavemax = (const.b_wien / temperature).to(u.AA)  # Wien's displacement law
waveset = np.logspace(
    0, np.log10(wavemax.value + 10 * wavemax.value), num=1000) * u.AA
with np.errstate(all='ignore'):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', AstropyDeprecationWarning)
        flux = blackbody_lambda(waveset, temperature)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(waveset.value, flux.value)
ax.axvline(wavemax.value, ls='--')
ax.get_yaxis().get_major_formatter().set_powerlimits((0, 1))
ax.set_xlabel(r'$\lambda$ ({0})'.format(waveset.unit))
ax.set_ylabel(r'$B_{\lambda}(T)$')
ax.set_title('Blackbody, T = {0}'.format(temperature))