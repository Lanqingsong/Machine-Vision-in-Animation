import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# Function to generate an ideal chessboard pattern
def generate_chessboard(rows, cols, square_size, img_size):
    board = np.zeros(img_size, dtype=np.uint8)
    center_x, center_y = img_size[1] // 2, img_size[0] // 2

    for r in range(rows):
        for c in range(cols):
            x_start = center_x - (cols // 2) * square_size + c * square_size
            y_start = center_y - (rows // 2) * square_size + r * square_size

            x_end = x_start + square_size
            y_end = y_start + square_size

            if (r + c) % 2 == 0:
                board[y_start:y_end, x_start:x_end] = 255
    return board


# Function to apply forward radial distortion (to create the "distorted" input image)
def apply_forward_radial_distortion(image, k1_true, k2_true):
    height, width = image.shape
    center_x, center_y = width / 2, height / 2

    distorted_image = np.zeros_like(image, dtype=np.uint8)

    # Iterate over each pixel in the undistorted image
    for y_u in range(height):
        for x_u in range(width):
            # Convert undistorted pixel (x_u, y_u) to normalized coordinates
            x_norm = (x_u - center_x) / center_x
            y_norm = (y_u - center_y) / center_y

            r_sq = x_norm ** 2 + y_norm ** 2

            # Apply distortion model to find its position in the distorted image
            distortion_factor = (1 + k1_true * r_sq + k2_true * r_sq ** 2)

            x_d_norm = x_norm * distortion_factor
            y_d_norm = y_norm * distortion_factor

            # Convert back to pixel coordinates in the distorted image
            x_d = int(x_d_norm * center_x + center_x)
            y_d = int(y_d_norm * center_y + center_y)

            # Ensure coordinates are within bounds
            if 0 <= x_d < width and 0 <= y_d < height:
                distorted_image[y_d, x_d] = image[y_u, x_u]
    return distorted_image


# Function to apply inverse radial distortion (for correction)
def apply_inverse_radial_distortion(image, k1_correct, k2_correct):
    height, width = image.shape
    center_x, center_y = width / 2, height / 2

    corrected_image = np.zeros_like(image, dtype=np.uint8)

    # Iterate over each pixel in the *corrected* image
    for y_c in range(height):
        for x_c in range(width):
            # Convert corrected pixel (x_c, y_c) to normalized coordinates
            x_norm_c = (x_c - center_x) / center_x
            y_norm_c = (y_c - center_y) / center_y

            # This is the tricky part for inverse mapping:
            # For accurate inverse, we'd solve for x_norm_d, y_norm_d such that
            # x_norm_c = x_norm_d * (1 + k1_correct * r_d^2 + k2_correct * r_d^4)
            # This usually requires iteration or approximation.
            # A common approximation for small distortions is to use the *same* formula but with negative coefficients,
            # or to assume the r_d is close to r_c.

            # Here, we use a simple iterative approach to find the source pixel in the *distorted* image
            x_distorted = x_norm_c
            y_distorted = y_norm_c

            # Iterate a few times to get closer to the true source pixel in the distorted image
            for _ in range(5):  # A few iterations for approximation
                r_sq_distorted = x_distorted ** 2 + y_distorted ** 2
                distortion_factor = (1 + k1_correct * r_sq_distorted + k2_correct * r_sq_distorted ** 2)
                x_distorted = x_norm_c / distortion_factor
                y_distorted = y_norm_c / distortion_factor

            # Convert back to pixel coordinates in the *original distorted* image
            src_x = int(x_distorted * center_x + center_x)
            src_y = int(y_distorted * center_y + center_y)

            # Ensure coordinates are within bounds
            if 0 <= src_x < width and 0 <= src_y < height:
                corrected_image[y_c, x_c] = image[src_y, src_x]
    return corrected_image


# --- Setup Plot ---
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
plt.subplots_adjust(left=0.1, bottom=0.3)

img_size = (400, 400)
chessboard_ideal = generate_chessboard(8, 8, 40, img_size)

# Create a truly distorted image to be corrected
# We'll use a known barrel distortion for this example
true_k1 = 0.2
true_k2 = -0.05
initial_distorted_input = apply_forward_radial_distortion(chessboard_ideal, true_k1, true_k2)

# Initial image display
img_display_left = axes[0].imshow(initial_distorted_input, cmap='gray')
axes[0].set_title('Original Distorted Image')
axes[0].set_xticks([]);
axes[0].set_yticks([])

# Start with no correction applied
corrected_img = apply_inverse_radial_distortion(initial_distorted_input, k1_correct=0, k2_correct=0)
img_display_right = axes[1].imshow(corrected_img, cmap='gray')
axes[1].set_title('Corrected Image (k1=0.0, k2=0.0)')
axes[1].set_xticks([]);
axes[1].set_yticks([])

# --- Sliders for Correction Coefficients ---
ax_k1_correct = plt.axes([0.15, 0.15, 0.7, 0.03])
k1_correct_slider = Slider(ax_k1_correct, 'Correction k1', -0.5, 0.5, valinit=0.0, valstep=0.01)

ax_k2_correct = plt.axes([0.15, 0.1, 0.7, 0.03])
k2_correct_slider = Slider(ax_k2_correct, 'Correction k2', -0.2, 0.2, valinit=0.0, valstep=0.005)


# --- Update Function ---
def update(val):
    current_k1_correct = k1_correct_slider.val
    current_k2_correct = k2_correct_slider.val

    new_corrected_img = apply_inverse_radial_distortion(initial_distorted_input, current_k1_correct, current_k2_correct)
    img_display_right.set_data(new_corrected_img)
    axes[1].set_title(f'Corrected Image (k1={current_k1_correct:.2f}, k2={current_k2_correct:.2f})')
    fig.canvas.draw_idle()


k1_correct_slider.on_changed(update)
k2_correct_slider.on_changed(update)

update(None)  # Initial call to set everything up

plt.show()