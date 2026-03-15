import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider


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


# Function to apply radial distortion
def apply_radial_distortion(image, k1, k2):
    height, width = image.shape
    center_x, center_y = width / 2, height / 2

    # Create an empty image for the distorted result
    distorted_image = np.zeros_like(image, dtype=np.uint8)

    # Iterate over each pixel in the distorted image
    for y_d in range(height):
        for x_d in range(width):
            # Convert distorted pixel (x_d, y_d) to normalized coordinates (from -1 to 1)
            x_norm = (x_d - center_x) / center_x
            y_norm = (y_d - center_y) / center_y

            r_sq = x_norm ** 2 + y_norm ** 2

            # Apply inverse distortion model to find source pixel in undistorted image
            # This is an approximation; ideally, it's an iterative solution
            # For direct mapping, we'd go from undistorted to distorted.
            # Here, we inverse map from distorted (x_d, y_d) to undistorted (x_u, y_u)
            # A simple approximation for sampling:
            distortion_factor = (1 + k1 * r_sq + k2 * r_sq ** 2)

            x_u_norm = x_norm / distortion_factor
            y_u_norm = y_norm / distortion_factor

            # Convert back to pixel coordinates in the original image
            x_u = int(x_u_norm * center_x + center_x)
            y_u = int(y_u_norm * center_y + center_y)

            # Ensure coordinates are within bounds
            if 0 <= x_u < width and 0 <= y_u < height:
                distorted_image[y_d, x_d] = image[y_u, x_u]
    return distorted_image


# Simulate measurement: simple horizontal line length
def measure_line(image, start_x, end_x, y_pos):
    # For a purely visual demo, we just highlight the line
    line_img = np.copy(image)
    if y_pos < line_img.shape[0]:
        line_img[y_pos, start_x:end_x] = 200  # Mark the line
    return line_img, (end_x - start_x)  # Return image with line and length


# --- Setup Plot ---
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
plt.subplots_adjust(left=0.1, bottom=0.3)

img_size = (400, 400)
chessboard_ideal = generate_chessboard(8, 8, 40, img_size)

# Initial image display
distorted_img = apply_radial_distortion(chessboard_ideal, k1=0, k2=0)  # Start with no distortion
img_display_left = axes[0].imshow(chessboard_ideal, cmap='gray')
axes[0].set_title('Ideal (Undistorted)')
axes[0].set_xticks([]);
axes[0].set_yticks([])

img_display_right = axes[1].imshow(distorted_img, cmap='gray')
axes[1].set_title('Distorted View (k1=0.0, k2=0.0)')
axes[1].set_xticks([]);
axes[1].set_yticks([])

# --- Sliders for Distortion Coefficients ---
ax_k1 = plt.axes([0.15, 0.15, 0.7, 0.03])
k1_slider = Slider(ax_k1, 'Radial k1 (Barrel/Pincushion)', -0.5, 0.5, valinit=0.0, valstep=0.01)

ax_k2 = plt.axes([0.15, 0.1, 0.7, 0.03])
k2_slider = Slider(ax_k2, 'Radial k2', -0.2, 0.2, valinit=0.0, valstep=0.005)

# --- Radio Buttons for Measurement Position ---
rax = plt.axes([0.02, 0.4, 0.08, 0.2])
radio_measure = RadioButtons(rax, ('Center', 'Edge'))
current_measure_pos = 'Center'  # Default measurement position

# --- Initial Measurement ---
measure_y_center = img_size[0] // 2
measure_x_start_center = img_size[1] // 2 - 40
measure_x_end_center = img_size[1] // 2 + 40
initial_ideal_len = measure_x_end_center - measure_x_start_center

measure_y_edge = img_size[0] // 2 + 100  # Closer to edge
measure_x_start_edge = img_size[1] // 2 - 40
measure_x_end_edge = img_size[1] // 2 + 40

# Overlay for measurement line
line_ideal, _ = measure_line(chessboard_ideal, measure_x_start_center, measure_x_end_center, measure_y_center)
line_distorted, _ = measure_line(distorted_img, measure_x_start_center, measure_x_end_center, measure_y_center)

line_overlay_left = axes[0].imshow(line_ideal, cmap='gray', alpha=1)
line_overlay_right = axes[1].imshow(line_distorted, cmap='gray', alpha=1)

measure_text_left = axes[0].text(0.5, 1.05, f'Ideal Length: {initial_ideal_len} px',
                                 transform=axes[0].transAxes, ha='center', color='black')
measure_text_right = axes[1].text(0.5, 1.05, f'Distorted Length: {initial_ideal_len} px',
                                  transform=axes[1].transAxes, ha='center', color='red')


# --- Update Function ---
def update(val):
    current_k1 = k1_slider.val
    current_k2 = k2_slider.val

    new_distorted_img = apply_radial_distortion(chessboard_ideal, current_k1, current_k2)
    img_display_right.set_data(new_distorted_img)

    # Update measurement
    if current_measure_pos == 'Center':
        measure_y = measure_y_center
        measure_x_start = measure_x_start_center
        measure_x_end = measure_x_end_center
    else:  # Edge
        measure_y = measure_y_edge
        measure_x_start = measure_x_start_edge
        measure_x_end = measure_x_end_edge

    # Re-measure on the distorted image
    # For a real measurement, we'd detect features. Here, we just apply the same pixel span
    # and show the visual distortion

    # To simulate the actual *distortion in length*, we need to see how far the pixels shift
    # This simplified demo will visually show the line on the distorted grid,
    # and the text will reflect the *apparent* length from the pixels sampled

    # A more accurate simulation for measurement effect would involve re-calculating points after distortion
    # For now, we highlight the same pixel span, but the underlying grid is distorted

    measured_len = measure_x_end - measure_x_start

    line_distorted_overlay, _ = measure_line(new_distorted_img, measure_x_start, measure_x_end, measure_y)
    line_overlay_right.set_data(line_distorted_overlay)

    # Update text to reflect visual distortion (simplified)
    # The actual length of the *marked segment* in pixels is constant here,
    # but the *physical* length it represents on the distorted grid changes.
    # We can highlight how the grid squares stretch/compress.

    if current_k1 > 0:  # Barrel distortion, center compressed, edge stretched
        if current_measure_pos == 'Center':
            display_len_distorted = measured_len * (1 - abs(current_k1) * 0.5)  # Approx visual compression
        else:
            display_len_distorted = measured_len * (1 + abs(current_k1) * 1.5)  # Approx visual stretching
    elif current_k1 < 0:  # Pincushion distortion, center stretched, edge compressed
        if current_measure_pos == 'Center':
            display_len_distorted = measured_len * (1 + abs(current_k1) * 0.5)
        else:
            display_len_distorted = measured_len * (1 - abs(current_k1) * 1.5)
    else:
        display_len_distorted = measured_len

    measure_text_right.set_text(f'Distorted Length: {display_len_distorted:.1f} px')
    axes[1].set_title(f'Distorted View (k1={current_k1:.2f}, k2={current_k2:.2f})')
    fig.canvas.draw_idle()


def measure_pos_callback(label):
    global current_measure_pos
    current_measure_pos = label
    update(None)  # Trigger update to change measurement line position


k1_slider.on_changed(update)
k2_slider.on_changed(update)
radio_measure.on_clicked(measure_pos_callback)

update(None)  # Initial call to set everything up

plt.show()