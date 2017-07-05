g6 = models.Gaussian1D(mean=110 * u.THz, stddev=10 * u.THz, amplitude=1 * u.Jy)

g6_fit = fitter(g6, x, y, equivalencies={'x': u.spectral()})

plt.plot(x, g6_fit(x, equivalencies={'x': u.spectral()}), 'b-')
plt.xlabel('Wavelength (microns)')
plt.ylabel('Flux density (mJy)')