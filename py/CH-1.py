import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.patches as patches

# Initialize the dashboard
fig = plt.figure(figsize=(14, 8), facecolor='#f0f2f5')
plt.subplots_adjust(left=0.1, bottom=0.35, right=0.9, top=0.9, wspace=0.4)

# Subplot 1: Macro View (Physical Sensor Size vs Lens Coverage)
ax_macro = fig.add_subplot(131)
# Subplot 2: Micro View (Single Pixel Light Bucket Size)
ax_micro = fig.add_subplot(132)
# Subplot 3: System View (Data Bandwidth Load)
ax_data = fig.add_subplot(133)


def update(val):
    res_h = s_res.val  # Horizontal Resolution (pixels)
    p_size = s_pixel.val  # Pixel Size (um)
    fps = s_fps.val  # Frame Rate (fps)

    # Logic Calculation
    # 1. Physical Dimensions (mm)
    sensor_w_mm = (res_h * p_size) / 1000
    sensor_h_mm = (res_h * 0.75 * p_size) / 1000

    # 2. Data Rate (MB/s) - Simplified: Res_H * Res_V * FPS / 10^6
    total_pixels = res_h * (res_h * 0.75)
    data_rate = (total_pixels * fps) / 1e6

    # --- Update Macro View ---
    ax_macro.clear()
    ax_macro.set_title("MACRO: Sensor vs Lens", fontsize=11, fontweight='bold')
    # Standard 1.1-inch lens limit (approx 17.6mm width)
    lens_limit = 17.6
    lens_circle = patches.Circle((lens_limit / 2, lens_limit * 0.375), lens_limit / 2,
                                 linewidth=2, edgecolor='#bdc3c7', facecolor='none', linestyle='--')
    ax_macro.add_patch(lens_circle)
    ax_macro.text(0, lens_limit * 0.8, "Lens Image Circle", color='#7f8c8d', fontsize=9)

    # Sensor Rect
    sensor_color = '#3498db' if sensor_w_mm <= lens_limit else '#e74c3c'
    rect = patches.Rectangle((0, 0), sensor_w_mm, sensor_h_mm, facecolor=sensor_color, alpha=0.7)
    ax_macro.add_patch(rect)
    ax_macro.set_xlim(-2, 25)
    ax_macro.set_ylim(-2, 20)
    ax_macro.set_xlabel("Width (mm)")
    ax_macro.text(0, -3, f"Size: {sensor_w_mm:.1f}x{sensor_h_mm:.1f}mm", fontweight='bold', color=sensor_color)

    # --- Update Micro View ---
    ax_micro.clear()
    ax_micro.set_title("MICRO: Pixel Sensitivity", fontsize=11, fontweight='bold')
    # Draw 3x3 pixels to show individual size
    for x in range(3):
        for y in range(3):
            p = patches.Rectangle((x * p_size, y * p_size), p_size * 0.9, p_size * 0.9,
                                  facecolor='#f39c12', edgecolor='black')
            ax_micro.add_patch(p)
    ax_micro.set_xlim(0, 35)
    ax_micro.set_ylim(0, 35)
    ax_micro.set_xlabel("Micrometers (um)")
    ax_micro.text(2, 32, f"Bucket Size: {p_size:.2f}um", color='#d35400', fontweight='bold')

    # --- Update Data View ---
    ax_data.clear()
    ax_data.set_title("SYSTEM: Data Bandwidth", fontsize=11, fontweight='bold')
    bw_limit = 600  # MB/s (typical USB3.0/GigE limit)
    bar_color = '#2ecc71' if data_rate < bw_limit else '#e74c3c'
    ax_data.bar(["Bandwidth"], [data_rate], color=bar_color)
    ax_data.axhline(bw_limit, color='black', linestyle='--')
    ax_data.set_ylim(0, 1200)
    ax_data.set_ylabel("MB/s")
    ax_data.text(-0.25, data_rate + 30, f"{data_rate:.1f}\nMB/s", fontweight='bold', ha='center')
    if data_rate > bw_limit:
        ax_data.text(-0.4, 1100, "OVERLOADED!", color='red', fontweight='bold')

    fig.canvas.draw_idle()


# Sliders setup
ax_color = '#ecf0f1'
s_res = Slider(plt.axes([0.2, 0.20, 0.6, 0.03], facecolor=ax_color), 'Resolution (H)', 640, 5000, valinit=2448,
               valfmt='%0.0f')
s_pixel = Slider(plt.axes([0.2, 0.15, 0.6, 0.03], facecolor=ax_color), 'Pixel Size (um)', 1.0, 10.0, valinit=3.45)
s_fps = Slider(plt.axes([0.2, 0.10, 0.6, 0.03], facecolor=ax_color), 'Frame Rate (FPS)', 1, 300, valinit=30,
               valfmt='%0.0f')

s_res.on_changed(update)
s_pixel.on_changed(update)
s_fps.on_changed(update)

update(None)
plt.show()