import numpy as np
import matplotlib.pyplot as plt

from astropy.modeling.models import BlackBody1D
from astropy.modeling.blackbody import FLAM
from astropy import units as u
from astropy.visualization import quantity_support

bb = BlackBody1D(temperature=5778*u.K)
wav = np.arange(1000, 110000) * u.AA
flux = bb(wav).to(FLAM, u.spectral_density(wav))

with quantity_support():
    plt.figure()
    plt.semilogx(wav, flux)
    plt.axvline(bb.lambda_max.to(u.AA).value, ls='--')
    plt.show()