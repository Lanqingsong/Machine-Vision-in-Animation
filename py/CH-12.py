import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

# --- Setup Plot ---
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(left=0.1, bottom=0.35, right=0.9, top=0.9)

# Initial parameters
initial_fov_mm = 100  # mm
initial_resolution_pixels = 640  # pixels (e.g., horizontal resolution)

# Calculate initial pixel equivalent
initial_pixel_equivalent = initial_fov_mm / initial_resolution_pixels

# --- Drawing Elements ---
# Real World FOV (Green Rectangle)
fov_rect_height = 50  # Visual height for FOV representation
fov_rect = plt.Rectangle((-initial_fov_mm / 2, 50), initial_fov_mm, fov_rect_height, color='green', alpha=0.6,
                         label='Field of View (FOV)')
ax.add_patch(fov_rect)
fov_text = ax.text(0, 50 + fov_rect_height + 5, f'FOV: {initial_fov_mm:.0f} mm', ha='center', va='bottom',
                   color='green')

# Simulated Object within FOV (Red Line)
object_width_mm = 20  # Fixed physical width of the object
object_line, = ax.plot([-object_width_mm / 2, object_width_mm / 2],
                       [50 + fov_rect_height / 2, 50 + fov_rect_height / 2], 'r-', linewidth=3, label='Object')
object_text_physical = ax.text(0, 50 + fov_rect_height / 2 - 10, f'Object: {object_width_mm:.0f} mm', ha='center',
                               va='top', color='red')

# Camera Sensor / Resolution (Blue Rectangle)
sensor_rect_height = 50  # Visual height for Sensor representation
sensor_rect_y = -50 - sensor_rect_height  # Position below 0
sensor_rect = plt.Rectangle((-initial_resolution_pixels / 2, sensor_rect_y), initial_resolution_pixels,
                            sensor_rect_height, color='blue', alpha=0.6, label='Camera Sensor (Resolution)')
ax.add_patch(sensor_rect)
resolution_text = ax.text(0, sensor_rect_y - 5, f'Resolution: {initial_resolution_pixels:.0f} pixels', ha='center',
                          va='top', color='blue')

# Pixels on Sensor (Vertical Lines)
pixel_lines = []
for i in range(initial_resolution_pixels + 1):
    x_pos = -initial_resolution_pixels / 2 + i
    line, = ax.plot([x_pos, x_pos], [sensor_rect_y, sensor_rect_y + sensor_rect_height], 'k:', linewidth=0.5, alpha=0.4)
    pixel_lines.append(line)

# Pixel Equivalent Value Display
pixel_eq_text = ax.text(0, 0, f'Pixel Equivalent: {initial_pixel_equivalent:.4f} mm/pixel', ha='center', va='center',
                        color='black', fontsize=12, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

# Simulated Measurement Bar (on the sensor/pixel grid)
# This will show the object's width *in pixels* and then convert to physical
# Pixels occupied by object
pixels_occupied_initial = object_width_mm / initial_pixel_equivalent
measurement_bar_y = sensor_rect_y - 30
measurement_bar, = ax.plot([-pixels_occupied_initial / 2, pixels_occupied_initial / 2],
                           [measurement_bar_y, measurement_bar_y], 'r-', linewidth=4)
measured_physical_text = ax.text(0, measurement_bar_y - 5,
                                 f'Measured: {pixels_occupied_initial:.1f} pixels -> {object_width_mm:.2f} mm',
                                 ha='center', va='top', color='red')

ax.set_aspect('equal', adjustable='box')
ax.set_title("Pixel Equivalent (Pixel Accuracy) Calculation")
ax.set_xticks([])
ax.set_yticks([])

# --- Sliders ---
ax_fov = plt.axes([0.15, 0.2, 0.7, 0.03])
fov_slider = Slider(ax_fov, 'Field of View (FOV) mm', 20, 500, valinit=initial_fov_mm, valstep=1)

ax_res = plt.axes([0.15, 0.15, 0.7, 0.03])
res_slider = Slider(ax_res, 'Resolution (pixels)', 100, 2000, valinit=initial_resolution_pixels, valstep=10)


# --- Update Function ---
def update(val):
    current_fov_mm = fov_slider.val
    current_resolution_pixels = int(res_slider.val)  # Ensure integer for pixel count

    # Calculate current pixel equivalent
    current_pixel_equivalent = current_fov_mm / current_resolution_pixels if current_resolution_pixels > 0 else 0

    # Update FOV Rectangle and Text
    fov_rect.set_x(-current_fov_mm / 2)
    fov_rect.set_width(current_fov_mm)
    fov_text.set_text(f'FOV: {current_fov_mm:.0f} mm')

    # Update Sensor Resolution Rectangle and Text
    # We dynamically adjust the width of the sensor rect to reflect the pixel count for visual clarity
    # Even though physical sensor size is fixed, for this demo we scale the visual width of the 'sensor'
    # to represent the number of pixels it has.
    sensor_rect.set_x(-current_resolution_pixels / 2)
    sensor_rect.set_width(current_resolution_pixels)
    resolution_text.set_text(f'Resolution: {current_resolution_pixels:.0f} pixels')

    # Update Pixel Lines (remove old, draw new)
    for line in pixel_lines:
        line.remove()
    pixel_lines.clear()
    for i in range(current_resolution_pixels + 1):
        x_pos = -current_resolution_pixels / 2 + i
        line, = ax.plot([x_pos, x_pos], [sensor_rect_y, sensor_rect_y + sensor_rect_height], 'k:', linewidth=0.5,
                        alpha=0.4)
        pixel_lines.append(line)

    # Update Pixel Equivalent Text
    pixel_eq_text.set_text(f'Pixel Equivalent: {current_pixel_equivalent:.4f} mm/pixel')

    # Update Simulated Measurement Bar
    # Calculate pixels occupied by object based on current pixel_equivalent
    pixels_occupied = object_width_mm / current_pixel_equivalent if current_pixel_equivalent > 0 else 0
    measurement_bar.set_xdata([-pixels_occupied / 2, pixels_occupied / 2])
    measured_physical_text.set_text(f'Measured: {pixels_occupied:.1f} pixels -> {object_width_mm:.2f} mm')

    # Adjust plot limits dynamically
    max_visual_width = max(current_fov_mm, current_resolution_pixels) * 1.2
    ax.set_xlim(-max_visual_width / 2, max_visual_width / 2)

    fig.canvas.draw_idle()


fov_slider.on_changed(update)
res_slider.on_changed(update)

update(None)  # Initial call to set everything up

plt.show()