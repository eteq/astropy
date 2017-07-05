import astropy.units as u
ax.coords[2].set_major_formatter('x.x') # Otherwise values round to the nearest whole number
ax.coords[2].set_format_unit(u.km / u.s)