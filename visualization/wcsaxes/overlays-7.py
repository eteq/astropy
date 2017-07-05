from matplotlib.patches import Circle

r = Rectangle((266.4, -28.9), 0.3, 0.3, edgecolor='cyan', facecolor='none',
              transform=ax.get_transform('fk5'))
ax.add_patch(r)

c = Circle((266.4, -29.1), 0.15, edgecolor='yellow', facecolor='none',
              transform=ax.get_transform('fk5'))
ax.add_patch(c)