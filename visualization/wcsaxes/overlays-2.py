# The following line makes it so that the zoom level no longer changes,
# otherwise Matplotlib has a tendency to zoom out when adding overlays.
ax.set_autoscale_on(False)

# Add a rectangle with bottom left corner at pixel position (30, 50) with a
# width and height of 60 and 50 pixels respectively.
from matplotlib.patches import Rectangle
r = Rectangle((30., 50.), 60., 50., edgecolor='yellow', facecolor='none')
ax.add_patch(r)

# Add three markers at (40, 30), (100, 130), and (130, 60). The facecolor is
# a transparent white (0.5 is the alpha value).
ax.scatter([40, 100, 130], [30, 130, 60], s=100, edgecolor='white', facecolor=(1, 1, 1, 0.5))