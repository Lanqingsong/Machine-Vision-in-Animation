import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- Setup Plot ---
fig, ax = plt.subplots(figsize=(12, 7))
plt.subplots_adjust(left=0.08, bottom=0.35, right=0.95, top=0.9)

# Initial parameters
focal_length = 50  # Lens focal length
lens_pos_x = 0  # Lens is at x=0
sensor_pos_x = focal_length  # Sensor is at focal_length from lens for parallel light, or more complex for close-up

# Fixed focus distance (where we want to be sharp)
# For simplicity, let's assume we are focusing at an object distance 'u_focus'
# Using thin lens formula: 1/f = 1/u + 1/v
# Let's fix the focus distance 'u_focus' and calculate 'v_focus' (sensor position)
initial_u_focus = -200  # Object at -200mm (left of lens)
initial_v_focus = 1 / (1 / focal_length + 1 / initial_u_focus) if initial_u_focus != 0 else focal_length
initial_sensor_pos_x = initial_v_focus

initial_aperture_diameter = 10  # Initial aperture diameter
initial_f_stop = focal_length / initial_aperture_diameter  # Calculate F-stop

# Non-focus object (will be blurry)
initial_u_non_focus = -150  # Another object at -150mm

# --- Drawing Elements ---
ax.axhline(0, color='gray', linestyle='--', linewidth=0.8, label='Optical Axis')

# Lens
lens_height_viz = 40  # Visual height of lens
lens_rect = plt.Rectangle((lens_pos_x - 2, -lens_height_viz / 2), 4, lens_height_viz, color='blue', alpha=0.6,
                          label='Lens')
ax.add_patch(lens_rect)
ax.text(lens_pos_x, -lens_height_viz / 2 - 5, f'Lens (f={focal_length}mm)', ha='center', va='top', color='blue')

# Aperture (represented by two lines on the lens plane)
aperture_line1, = ax.plot([lens_pos_x, lens_pos_x], [initial_aperture_diameter / 2, lens_height_viz / 2], 'k-',
                          linewidth=2)
aperture_line2, = ax.plot([lens_pos_x, lens_pos_x], [-initial_aperture_diameter / 2, -lens_height_viz / 2], 'k-',
                          linewidth=2)
aperture_text = ax.text(lens_pos_x + 5, initial_aperture_diameter / 2 + 5,
                        f'Aperture: {initial_aperture_diameter:.1f}mm (F/{initial_f_stop:.1f})', ha='left', va='bottom',
                        color='black')

# Focus Object Point (Red dot on the left)
focus_object_point, = ax.plot(initial_u_focus, 0, 'ro', markersize=8, label='Focus Object')
ax.text(initial_u_focus, 5, 'Focus Object', ha='center', va='bottom', color='red')

# Non-Focus Object Point (Orange dot on the left)
non_focus_object_point, = ax.plot(initial_u_non_focus, 10, 'o', color='orange', markersize=8, label='Non-Focus Object')
ax.text(initial_u_non_focus, 15, 'Non-Focus Object', ha='center', va='bottom', color='orange')

# Sensor Plane (Image Plane)
sensor_rect = plt.Rectangle((initial_sensor_pos_x - 2, -20), 4, 40, color='green', alpha=0.7, label='Sensor Plane')
ax.add_patch(sensor_rect)
sensor_text = ax.text(initial_sensor_pos_x, -25, f'Sensor (Focus V: {initial_sensor_pos_x:.1f}mm)', ha='center',
                      va='top', color='green')

# Rays from FOCUS Object (should converge to a point on sensor)
# Ray from focus object top aperture edge
ray_focus1, = ax.plot([initial_u_focus, lens_pos_x, initial_sensor_pos_x],
                      [0, initial_aperture_diameter / 2, 0], 'r--', alpha=0.4)
# Ray from focus object bottom aperture edge
ray_focus2, = ax.plot([initial_u_focus, lens_pos_x, initial_sensor_pos_x],
                      [0, -initial_aperture_diameter / 2, 0], 'r--', alpha=0.4)

# Rays from NON-FOCUS Object (will form a circle of confusion on sensor)
# Object point is at (initial_u_non_focus, initial_object_height_non_focus)
# Ray through top aperture edge
ray_non_focus1, = ax.plot([initial_u_non_focus, lens_pos_x, initial_sensor_pos_x],
                          [10, initial_aperture_diameter / 2, 0], 'o--', color='orange', alpha=0.6)
# Ray through bottom aperture edge
ray_non_focus2, = ax.plot([initial_u_non_focus, lens_pos_x, initial_sensor_pos_x],
                          [10, -initial_aperture_diameter / 2, 0], 'o--', color='orange', alpha=0.6)

# Circle of Confusion (CoC) visualization
coc_line, = ax.plot([], [], 'o', color='purple', markersize=0, label='CoC')  # Placeholder for plotting
coc_text = ax.text(initial_sensor_pos_x + 5, 0, 'CoC Diameter: 0.0mm', ha='left', va='center', color='purple')

# Adjust plot limits
ax.set_xlim(-300, 150)
ax.set_ylim(-100, 100)
ax.set_aspect('equal', adjustable='box')
ax.set_title("Aperture, Focus, and Blur (Circle of Confusion)")
ax.set_xticks([])
ax.set_yticks([])

# --- Sliders ---
ax_aperture = plt.axes([0.15, 0.2, 0.7, 0.03])
aperture_slider = Slider(ax_aperture, 'Aperture Diameter (mm)', 1, 40, valinit=initial_aperture_diameter, valstep=0.5)

ax_non_focus_dist = plt.axes([0.15, 0.15, 0.7, 0.03])
non_focus_dist_slider = Slider(ax_non_focus_dist, 'Non-Focus Object Distance (mm)', -300, -100,
                               valinit=initial_u_non_focus, valstep=5)


# --- Update Function ---
def update(val):
    current_aperture_diameter = aperture_slider.val
    current_u_non_focus = non_focus_dist_slider.val

    # Update Aperture Visual
    aperture_line1.set_ydata([current_aperture_diameter / 2, lens_height_viz / 2])
    aperture_line2.set_ydata([-current_aperture_diameter / 2, -lens_height_viz / 2])

    current_f_stop = focal_length / current_aperture_diameter
    aperture_text.set_text(f'Aperture: {current_aperture_diameter:.1f}mm (F/{current_f_stop:.1f})')

    # Update Non-Focus Object position
    non_focus_object_point.set_xdata([current_u_non_focus])
    ax.texts[4].set_x(current_u_non_focus)  # Update text for non-focus object

    # --- Recalculate Rays and CoC for Non-Focus Object ---
    # Object height on non-focus plane (y_o)
    y_o_non_focus = 10

    # Coordinates of aperture edges
    y_aperture_top = current_aperture_diameter / 2
    y_aperture_bottom = -current_aperture_diameter / 2

    # Calculate where rays from non-focus object intersect sensor plane
    # Ray through top of aperture: (x1, y1) = (u_non_focus, y_o_non_focus) to (x2, y2) = (lens_pos_x, y_aperture_top)
    # Slope m = (y2 - y1) / (x2 - x1)
    # y_intersect = y1 + m * (sensor_pos_x - x1)

    # Top ray intersection y-coord on sensor
    m_top = (y_aperture_top - y_o_non_focus) / (lens_pos_x - current_u_non_focus)
    y_intersect_top = y_o_non_focus + m_top * (initial_sensor_pos_x - current_u_non_focus)

    # Bottom ray intersection y-coord on sensor
    m_bottom = (y_aperture_bottom - y_o_non_focus) / (lens_pos_x - current_u_non_focus)
    y_intersect_bottom = y_o_non_focus + m_bottom * (initial_sensor_pos_x - current_u_non_focus)

    coc_diameter = abs(y_intersect_top - y_intersect_bottom)

    # Update Non-Focus Rays
    ray_non_focus1.set_xdata([current_u_non_focus, lens_pos_x, initial_sensor_pos_x])
    ray_non_focus1.set_ydata([y_o_non_focus, y_aperture_top, y_intersect_top])

    ray_non_focus2.set_xdata([current_u_non_focus, lens_pos_x, initial_sensor_pos_x])
    ray_non_focus2.set_ydata([y_o_non_focus, y_aperture_bottom, y_intersect_bottom])

    # Update CoC Visualization
    coc_x_data = [initial_sensor_pos_x] * 2
    coc_y_data = [y_intersect_bottom, y_intersect_top]
    coc_line.set_xdata(coc_x_data)
    coc_line.set_ydata(coc_y_data)
    coc_line.set_markersize(8)  # Make dots visible
    coc_line.set_linestyle('')  # No line connecting

    coc_text.set_text(f'CoC Diameter: {coc_diameter:.2f}mm')

    fig.canvas.draw_idle()


aperture_slider.on_changed(update)
non_focus_dist_slider.on_changed(update)

update(None)  # Initial call to set everything up

plt.show()