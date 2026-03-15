import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Create a figure and a set of subplots
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(left=0.1, bottom=0.35)

# Simulate a scene with varying brightness
# A simple horizontal gradient from dark to light
scene_brightness = np.linspace(0, 1, 256).reshape(1, -1)
scene_brightness = np.tile(scene_brightness, (100, 1))

# Initial camera parameters
initial_dynamic_range = 8  # in stops
initial_exposure_offset = 0.5  # 0 to 1, maps scene brightness to output range


# Function to simulate camera sensor response
def simulate_camera_response(scene, dr_stops, exposure_offset):
    min_log_brightness = np.log2(0.001)  # Simulate a very dark lower bound
    max_log_brightness = np.log2(1.0)  # Simulate a very bright upper bound

    # Convert scene brightness (0-1) to a wider log scale
    log_scene = np.log2(scene * (max_log_brightness - min_log_brightness) + 2 ** min_log_brightness)

    # Calculate sensor's detectable range
    sensor_min_val = exposure_offset * (max_log_brightness - min_log_brightness) + min_log_brightness - dr_stops / 2
    sensor_max_val = sensor_min_val + dr_stops

    # Clamp the log scene to the sensor's range
    output_log_scene = np.clip(log_scene, sensor_min_val, sensor_max_val)

    # Normalize to 0-1 for display
    normalized_output = (output_log_scene - sensor_min_val) / (sensor_max_val - sensor_min_val)

    # Identify overexposed and underexposed areas
    overexposed = log_scene > sensor_max_val
    underexposed = log_scene < sensor_min_val

    return normalized_output, overexposed, underexposed


# Initial image display
simulated_image, overexposed_mask, underexposed_mask = simulate_camera_response(
    scene_brightness, initial_dynamic_range, initial_exposure_offset
)
img_display = ax.imshow(simulated_image, cmap='gray', vmin=0, vmax=1, aspect='auto')
ax.set_title(f'Simulated Camera View (DR: {initial_dynamic_range} stops, Exp: {initial_exposure_offset:.2f})')
ax.set_xticks([])
ax.set_yticks([])

# Add overlays for over/underexposure
over_overlay = ax.imshow(overexposed_mask, cmap='Reds', alpha=0.3, aspect='auto')
under_overlay = ax.imshow(underexposed_mask, cmap='Blues', alpha=0.3, aspect='auto')

# Sliders for dynamic range and exposure
ax_dr = plt.axes([0.1, 0.2, 0.8, 0.03])
dr_slider = Slider(ax_dr, 'Dynamic Range (stops)', 1, 16, valinit=initial_dynamic_range, valstep=1)

ax_exp = plt.axes([0.1, 0.15, 0.8, 0.03])
exp_slider = Slider(ax_exp, 'Exposure Offset', 0, 1, valinit=initial_exposure_offset, valstep=0.01)


# Update function for sliders
def update(val):
    current_dr = dr_slider.val
    current_exp = exp_slider.val

    new_image, new_overexposed, new_underexposed = simulate_camera_response(
        scene_brightness, current_dr, current_exp
    )
    img_display.set_data(new_image)
    over_overlay.set_data(new_overexposed)
    under_overlay.set_data(new_underexposed)
    ax.set_title(f'Simulated Camera View (DR: {current_dr} stops, Exp: {current_exp:.2f})')
    fig.canvas.draw_idle()


dr_slider.on_changed(update)
exp_slider.on_changed(update)

plt.show()