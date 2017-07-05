filename = get_pkg_data_filename('galactic_center/gc_bolocam_gps.fits')
hdu = fits.open(filename)[0]
ax.contour(hdu.data, transform=ax.get_transform(WCS(hdu.header)),
           levels=[1,2,3,4,5,6], colors='white')