import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- Setup Plot ---
fig, ax = plt.subplots(figsize=(12, 7))
plt.subplots_adjust(left=0.08, bottom=0.35, right=0.95, top=0.9)

# Initial parameters
initial_focal_length = 25  # mm
initial_working_distance = 500  # mm
initial_sensor_size = 8.8  # mm (e.g., 1/2.5" sensor horizontal)

# Calculate initial FOV and image size on sensor
# FOV = (WD * S) / f
initial_fov = (initial_working_distance * initial_sensor_size) / initial_focal_length
# Image size on sensor is always equal to sensor_size if FOV perfectly covers it,
# but we are showing the *portion* of the sensor used or the *scale* of imaging
# For simplicity, we directly show sensor size as the image height.
# The horizontal spread is the actual image across the sensor.

# --- Drawing Elements ---
# Optical Axis
ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)

# Lens (positioned at X=0, Y=0)
lens_x = 0
lens_width = 10  # Visual width of the lens
lens_height = 20  # Visual height of the lens
lens_rect = plt.Rectangle((lens_x - lens_width / 2, -lens_height / 2), lens_width, lens_height, color='blue', alpha=0.6,
                          label='Lens')
ax.add_patch(lens_rect)
ax.text(lens_x, -lens_height / 2 - 5, 'Lens (f)', ha='center', va='top', color='blue')

# Object Plane (Working Distance) - on the left
object_x = -initial_working_distance
object_height = initial_fov  # Initial FOV as object height
object_rect = plt.Rectangle((object_x - 2, -object_height / 2), 4, object_height, color='red', alpha=0.7,
                            label='Object (FOV)')
ax.add_patch(object_rect)
object_text = ax.text(object_x, -object_height / 2 - 10, f'FOV: {initial_fov:.1f} mm', ha='center', va='top',
                      color='red')
object_wd_text = ax.text(object_x / 2, -lens_height / 2 - 5, f'WD: {initial_working_distance:.0f} mm', ha='center',
                         va='top', color='black')

# Sensor Plane (Image Plane) - on the right
sensor_x = initial_focal_length  # Position of sensor from lens
sensor_height = initial_sensor_size  # Sensor physical height
sensor_rect = plt.Rectangle((sensor_x - 2, -sensor_height / 2), 4, sensor_height, color='green', alpha=0.7,
                            label='Sensor (S)')
ax.add_patch(sensor_rect)
sensor_text = ax.text(sensor_x, -sensor_height / 2 - 10, f'Sensor S: {initial_sensor_size:.1f} mm', ha='center',
                      va='top', color='green')
# text for focal length behind sensor
focal_length_text = ax.text(sensor_x / 2, lens_height / 2 + 5, f'f: {initial_focal_length:.0f} mm', ha='center',
                            va='bottom', color='black')

# Rays (from object edges through lens center to sensor edges)
# Object top -> Lens center -> Sensor top
ray1, = ax.plot([object_x, lens_x, sensor_x], [object_height / 2, 0, -sensor_height / 2], 'k--', alpha=0.6)
# Object bottom -> Lens center -> Sensor bottom
ray2, = ax.plot([object_x, lens_x, sensor_x], [-object_height / 2, 0, sensor_height / 2], 'k--', alpha=0.6)

# Scale for axes
ax_min_x = min(object_x, -lens_width / 2) - 50
ax_max_x = max(sensor_x, lens_width / 2) + 50
ax_min_y = -max(object_height, sensor_height, lens_height) / 2 - 30
ax_max_y = max(object_height, sensor_height, lens_height) / 2 + 30

ax.set_xlim(ax_min_x, ax_max_x)
ax.set_ylim(ax_min_y, ax_max_y)
ax.set_aspect('equal', adjustable='box')
ax.set_title("Interactive Lens Parameters (f, WD, S, FOV)")
ax.set_xticks([])
ax.set_yticks([])

# --- Sliders ---
ax_f = plt.axes([0.15, 0.2, 0.7, 0.03])
f_slider = Slider(ax_f, 'Focal Length (f)', 5, 100, valinit=initial_focal_length, valstep=1)

ax_wd = plt.axes([0.15, 0.15, 0.7, 0.03])
wd_slider = Slider(ax_wd, 'Working Distance (WD)', 100, 1000, valinit=initial_working_distance, valstep=10)

ax_s = plt.axes([0.15, 0.1, 0.7, 0.03])
s_slider = Slider(ax_s, 'Sensor Size (S)', 2, 20, valinit=initial_sensor_size, valstep=0.1)


# --- Update Function ---
def update(val):
    current_f = f_slider.val
    current_wd = wd_slider.val
    current_s = s_slider.val

    # Recalculate FOV based on current parameters
    # FOV = (WD * S) / f
    current_fov = (current_wd * current_s) / current_f

    # Update Object Plane (FOV)
    object_x = -current_wd
    object_height = current_fov
    object_rect.set_x(object_x - 2)
    object_rect.set_y(-object_height / 2)
    object_rect.set_height(object_height)
    object_text.set_x(object_x)
    object_text.set_y(-object_height / 2 - 10)
    object_text.set_text(f'FOV: {current_fov:.1f} mm')
    object_wd_text.set_x(object_x / 2)
    object_wd_text.set_text(f'WD: {current_wd:.0f} mm')

    # Update Sensor Plane (S)
    sensor_x = current_f
    sensor_height = current_s
    sensor_rect.set_x(sensor_x - 2)
    sensor_rect.set_y(-sensor_height / 2)
    sensor_rect.set_height(sensor_height)
    sensor_text.set_x(sensor_x)
    sensor_text.set_y(-sensor_height / 2 - 10)
    sensor_text.set_text(f'Sensor S: {current_s:.1f} mm')
    focal_length_text.set_x(sensor_x / 2)
    focal_length_text.set_text(f'f: {current_f:.0f} mm')

    # Update Rays
    ray1.set_xdata([object_x, lens_x, sensor_x])
    ray1.set_ydata([object_height / 2, 0, -sensor_height / 2])  # Note: sensor image is inverted
    ray2.set_xdata([object_x, lens_x, sensor_x])
    ray2.set_ydata([-object_height / 2, 0, sensor_height / 2])  # Note: sensor image is inverted

    # Adjust plot limits dynamically
    current_max_height = max(object_height, sensor_height, lens_height)
    ax.set_xlim(min(object_x, -lens_width / 2) - 50, max(sensor_x, lens_width / 2) + 50)
    ax.set_ylim(-current_max_height / 2 - 30, current_max_height / 2 + 30)

    fig.canvas.draw_idle()


f_slider.on_changed(update)
wd_slider.on_changed(update)
s_slider.on_changed(update)

update(None)  # Initial call to set everything up

plt.show()