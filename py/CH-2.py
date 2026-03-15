import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.patches as patches
import numpy as np

# Setup Figure
fig = plt.figure(figsize=(14, 8), facecolor='#f8f9fa')
plt.subplots_adjust(left=0.1, bottom=0.35, right=0.9, top=0.9, wspace=0.3)

# Subplot 1: Physical FOV View
ax_fov = fig.add_subplot(121)
# Subplot 2: Zoomed Pixel View (Digital Representation)
ax_pixel = fig.add_subplot(122)


def update(val):
    fov_w = s_fov.val  # Field of View Width (mm)
    d_min = s_dmin.val  # Min Defect Size (mm)
    k_factor = s_k.val  # Accuracy Factor (k)

    # Calculation Logic
    # 1. Required Pixels (One dimension)
    req_pixels_h = (fov_w / d_min) * k_factor
    req_pixels_v = req_pixels_h * 0.75  # Assume 4:3
    total_mp = (req_pixels_h * req_pixels_v) / 1e6

    # 2. Pixel Accuracy (mm/pixel)
    pixel_acc = fov_w / req_pixels_h

    # --- Update FOV View ---
    ax_fov.clear()
    ax_fov.set_title("PHYSICAL VIEW: Field of View (FOV)", fontsize=12, fontweight='bold')
    # Draw FOV area
    fov_rect = patches.Rectangle((0, 0), fov_w, fov_w * 0.75, facecolor='#ecf0f1', edgecolor='#2c3e50', lw=2)
    ax_fov.add_patch(fov_rect)
    # Draw the defect (represented as a small red dot in the center)
    defect = patches.Circle((fov_w / 2, fov_w * 0.375), d_min / 2, color='#e74c3c', label='Defect')
    ax_fov.add_patch(defect)

    ax_fov.set_xlim(-10, 210)
    ax_fov.set_ylim(-10, 160)
    ax_fov.set_xlabel("Width (mm)")
    ax_fov.text(5, -20, f"Target Resolution: {req_pixels_h:.0f} x {req_pixels_v:.0f}\nTotal: {total_mp:.2f} Megapixels",
                fontsize=11, color='#2980b9', fontweight='bold')

    # --- Update Zoomed Pixel View ---
    ax_pixel.clear()
    ax_pixel.set_title(f"DIGITAL VIEW: Defect represented by {k_factor:.1f}x{k_factor:.1f} Pixels",
                       fontsize=12, fontweight='bold')

    # In this view, we show how the defect is "chopped" by pixels
    # We normalize the view to the defect size
    grid_res = int(k_factor * 2)  # Show a small area around the defect
    if grid_res < 5: grid_res = 5

    for x in range(grid_res):
        for y in range(grid_res):
            # Draw pixel grid
            color = '#3498db' if (
                        grid_res / 4 <= x <= grid_res * 3 / 4 and grid_res / 4 <= y <= grid_res * 3 / 4) else 'white'
            alpha = 0.5 if color == '#3498db' else 0.1
            p = patches.Rectangle((x, y), 1, 1, facecolor=color, edgecolor='gray', alpha=alpha)
            ax_pixel.add_patch(p)

    # Draw the defect circle over the pixels
    circ = patches.Circle((grid_res / 2, grid_res / 2), k_factor / 2, color='#e74c3c', alpha=0.6)
    ax_pixel.add_patch(circ)

    ax_pixel.set_xlim(0, grid_res)
    ax_pixel.set_ylim(0, grid_res)
    ax_pixel.set_xticks([])
    ax_pixel.set_yticks([])
    ax_pixel.text(0.5, -0.5, f"Pixel Accuracy: {pixel_acc:.4f} mm/pixel", fontsize=10)

    fig.canvas.draw_idle()


# UI Sliders
ax_color = '#f1c40f'
s_fov = Slider(plt.axes([0.2, 0.20, 0.6, 0.03], facecolor=ax_color), 'FOV Width (mm)', 10, 200, valinit=100)
s_dmin = Slider(plt.axes([0.2, 0.15, 0.6, 0.03], facecolor=ax_color), 'Min Defect (mm)', 0.05, 2.0, valinit=0.5)
s_k = Slider(plt.axes([0.2, 0.10, 0.6, 0.03], facecolor=ax_color), 'K Factor (Safety)', 1.0, 5.0, valinit=2.5)

s_fov.on_changed(update)
s_dmin.on_changed(update)
s_k.on_changed(update)

update(None)
plt.show()