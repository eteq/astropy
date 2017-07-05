from astropy.convolution import Gaussian2DKernel, interpolate_replace_nans

# Select a random set of pixels that were affected by some sort of artifact
# and replaced with NaNs (e.g., cosmic-ray-affected pixels)
np.random.seed(42)
yinds, xinds = np.indices(img.shape)
img[np.random.choice(yinds.flat, 50), np.random.choice(xinds.flat, 50)] = np.nan

# We smooth with a Gaussian kernel with stddev=1
# It is a 9x9 array
kernel = Gaussian2DKernel(stddev=1)

# interpolate away the NaNs
reconstructed_image = interpolate_replace_nans(img, kernel)


# apply peak-finding
kernel = CustomKernel([[-1,-1,-1], [-1, 8, -1], [-1,-1,-1]])

# Use the peak-finding kernel
# We have to turn off kernel normalization and set nan_treatment to "fill"
# here because `nan_treatment='interpolate'` is incompatible with non-
# normalized kernels
peaked_image = convolve(reconstructed_image, kernel,
                        normalize_kernel=False,
                        nan_treatment='fill')

plt.figure(1, figsize=(12, 12)).clf()
ax1 = plt.subplot(1, 3, 1)
ax1.set_title("Image with missing data")
im = ax1.imshow(img, vmin=-6., vmax=5.e1, origin='lower',
                interpolation='nearest', cmap='viridis')

ax2 = plt.subplot(1, 3, 2)
ax2.set_title("Interpolated")
im = ax2.imshow(reconstructed_image, vmin=-6., vmax=5.e1, origin='lower',
                interpolation='nearest', cmap='viridis')

ax3 = plt.subplot(1, 3, 3)
ax3.set_title("Peak-Finding")
im = ax3.imshow(peaked_image, vmin=-6., vmax=5.e1, origin='lower',
                interpolation='nearest', cmap='viridis')