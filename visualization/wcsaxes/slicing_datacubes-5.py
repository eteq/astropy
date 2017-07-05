ax = plt.subplot(projection=wcs, slices=(50, 'x', 'y'))
ax.imshow(image_data[:, :, 50])