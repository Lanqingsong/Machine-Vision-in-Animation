import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image

# Load the provided image (1.png)
try:
    img_path = '1.png'
    base_image = Image.open(img_path).convert('L')  # Convert to grayscale for simplicity
    base_image_np = np.array(base_image) / 255.0  # Normalize to 0-1
except FileNotFoundError:
    print(f"Error: {img_path} not found. Generating a synthetic image.")
    # Fallback to a synthetic image if 1.png is not found
    x = np.linspace(-1, 1, 256)
    y = np.linspace(-1, 1, 256)
    X, Y = np.meshgrid(x, y)
    base_image_np = (np.sin(X * 10) + np.cos(Y * 10) + 2) / 4  # Creates a patterned image
    base_image_np = np.sqrt(base_image_np)  # Make some parts brighter

if base_image_np.shape[0] < 100 or base_image_np.shape[1] < 100:
    base_image_np = np.repeat(np.repeat(base_image_np, 2, axis=0), 2, axis=1)
if base_image_np.max() == base_image_np.min():
    base_image_np[0, 0] = 0.5  # Avoid flat images


# Generate different exposure versions
def generate_exposure(image, exposure_factor):
    return np.clip(image * exposure_factor, 0, 1)


exposure_factors = [0.25, 1.0, 4.0]  # Under, Normal, Over
exposure_titles = ["Underexposed (Factor: 0.25)", "Normal Exposure (Factor: 1.0)", "Overexposed (Factor: 4.0)"]
exposed_images = [generate_exposure(base_image_np, f) for f in exposure_factors]


# HDR fusion function (simple weighted average for demonstration)
def fuse_hdr(images, exposure_factors):
    fused_image = np.zeros_like(images[0])
    weights = []

    # Simple weighting based on pixel intensity, avoiding clipping
    for img in images:
        weight = np.exp(-((img - 0.5) ** 2) / (2 * 0.1 ** 2))  # Gaussian weight centered at mid-gray
        weights.append(weight)

    total_weight = np.sum(weights, axis=0)
    total_weight[total_weight == 0] = 1e-6  # Avoid division by zero

    for i, img in enumerate(images):
        fused_image += (img * weights[i]) / total_weight

    return fused_image


fused_hdr_image = fuse_hdr(exposed_images, exposure_factors)

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
ims = []

# Initial display of individual exposures and an empty slot for HDR
for i, ax in enumerate(axes[:-1]):
    im = ax.imshow(exposed_images[i], cmap='gray', vmin=0, vmax=1)
    ax.set_title(exposure_titles[i])
    ax.set_xticks([])
    ax.set_yticks([])
    ims.append(im)

# Placeholder for the final HDR image
hdr_im = axes[-1].imshow(np.zeros_like(base_image_np), cmap='gray', vmin=0, vmax=1)
axes[-1].set_title("Fused HDR Image")
axes[-1].set_xticks([])
axes[-1].set_yticks([])
ims.append(hdr_im)

fig.suptitle("Multi-Exposure HDR Fusion Demonstration")


def update(frame):
    if frame == 0:
        # Initial state: only individual exposures visible
        for i in range(len(exposed_images)):
            ims[i].set_data(exposed_images[i])
        ims[-1].set_data(np.zeros_like(base_image_np))  # Clear HDR slot
        axes[-1].set_title("Fused HDR Image (Processing...)")
    elif frame == 1:
        # Show the fused HDR image
        ims[-1].set_data(fused_hdr_image)
        axes[-1].set_title("Fused HDR Image (Done!)")

    return ims


ani = FuncAnimation(fig, update, frames=[0, 1], interval=2000, blit=True, repeat=False)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()