import numpy as np
from time import time
from astropy.modeling import models
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

imshape = (300, 400)
y, x = np.indices(imshape)

# Generate random source model list
np.random.seed(0)
nsrc = 100
model_params = [
    dict(amplitude=np.random.uniform(.5, 1),
         x_mean=np.random.uniform(0, imshape[1] - 1),
         y_mean=np.random.uniform(0, imshape[0] - 1),
         x_stddev=np.random.uniform(2, 6),
         y_stddev=np.random.uniform(2, 6),
         theta=np.random.uniform(0, 2 * np.pi))
    for _ in range(nsrc)]

model_list = [models.Gaussian2D(**kwargs) for kwargs in model_params]

# Render models to image using bounding boxes
bb_image = np.zeros(imshape)
t_bb = time()
for model in model_list:
    model.render(bb_image)
t_bb = time() - t_bb

# Render models to image using full evaluation
full_image = np.zeros(imshape)
t_full = time()
for model in model_list:
    model.bounding_box = None
    model.render(full_image)
t_full = time() - t_full

flux = full_image.sum()
diff = (full_image - bb_image)
max_err = diff.max()

# Plots
plt.figure(figsize=(16, 7))
plt.subplots_adjust(left=.05, right=.97, bottom=.03, top=.97, wspace=0.15)

# Full model image
plt.subplot(121)
plt.imshow(full_image, origin='lower')
plt.title('Full Models\nTiming: {:.2f} seconds'.format(t_full), fontsize=16)
plt.xlabel('x')
plt.ylabel('y')

# Bounded model image with boxes overplotted
ax = plt.subplot(122)
plt.imshow(bb_image, origin='lower')
for model in model_list:
    del model.bounding_box  # Reset bounding_box to its default
    dy, dx = np.diff(model.bounding_box).flatten()
    pos = (model.x_mean.value - dx / 2, model.y_mean.value - dy / 2)
    r = Rectangle(pos, dx, dy, edgecolor='w', facecolor='none', alpha=.25)
    ax.add_patch(r)
plt.title('Bounded Models\nTiming: {:.2f} seconds'.format(t_bb), fontsize=16)
plt.xlabel('x')
plt.ylabel('y')

# Difference image
plt.figure(figsize=(16, 8))
plt.subplot(111)
plt.imshow(diff, vmin=-max_err, vmax=max_err)
plt.colorbar(format='%.1e')
plt.title('Difference Image\nTotal Flux Err = {:.0e}'.format(
    ((flux - np.sum(bb_image)) / flux)))
plt.xlabel('x')
plt.ylabel('y')
plt.show()