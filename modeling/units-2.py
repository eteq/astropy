from astropy.modeling import models, fitting

g5 = models.Gaussian1D(mean=3 * u.micron, stddev=1 * u.micron, amplitude=1 * u.Jy)

fitter = fitting.LevMarLSQFitter()

g5_fit = fitter(g5, x, y)

plt.plot(x, y, 'ko')
plt.plot(x, g5_fit(x), 'r-')
plt.xlabel('Wavelength (microns)')
plt.ylabel('Flux density (mJy)')