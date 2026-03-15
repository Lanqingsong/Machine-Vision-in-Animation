import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.patches as patches

# 1. Setup Figure
fig, ax = plt.subplots(figsize=(12, 7), facecolor='#f4f7f6')
plt.subplots_adjust(left=0.1, bottom=0.3, right=0.9, top=0.9)


def update(val):
    wd = s_wd.val  # Working Distance (mm)
    fov = s_fov.val  # Field of View (mm)
    sensor_s = s_sensor.val  # Sensor Size (mm)

    # Calculation: f = (WD * S) / FOV
    f_calc = (wd * sensor_s) / fov

    ax.clear()
    ax_title = f"LENS OPTICS: Focal Length Calculation\nCalculated f = {f_calc:.2f} mm"
    ax.set_title(ax_title, fontsize=14, fontweight='bold', color='#2c3e50')

    # --- Drawing Logic: Similar Triangles ---
    # Lens position is at x=0
    # Object is at x = -WD
    # Sensor is at x = f_calc (magnified for visibility)

    # 1. Draw Object (FOV)
    ax.plot([-wd, -wd], [-fov / 2, fov / 2], color='#e74c3c', lw=4, label='Object (FOV)')
    ax.text(-wd, fov / 2 + 5, f"FOV: {fov}mm", ha='center', color='#e74c3c')

    # 2. Draw Sensor (S)
    # Note: Sensor is drawn at x = f_calc * 5 for better visualization scale
    vis_f = f_calc * 5
    ax.plot([vis_f, vis_f], [-sensor_s / 2 * 5, sensor_s / 2 * 5], color='#3498db', lw=4, label='Sensor (S)')
    ax.text(vis_f, (sensor_s / 2 * 5) + 5, f"Sensor: {sensor_s}mm", ha='center', color='#3498db')

    # 3. Draw Lens (The center point)
    ax.scatter(0, 0, s=200, color='#2c3e50', marker='D', label='Lens Center')

    # 4. Draw Light Rays (Triangles)
    # Object to Lens
    ax.plot([-wd, 0, -wd], [fov / 2, 0, -fov / 2], color='gray', alpha=0.3, ls='--')
    # Lens to Sensor
    ax.plot([vis_f, 0, vis_f], [sensor_s / 2 * 5, 0, -sensor_s / 2 * 5], color='gray', alpha=0.3, ls='--')

    # 5. Dimension Arrows
    ax.annotate('', xy=(0, -10), xytext=(-wd, -10), arrowprops=dict(arrowstyle='<->'))
    ax.text(-wd / 2, -25, f"WD: {wd}mm", ha='center')

    ax.annotate('', xy=(vis_f, -10), xytext=(0, -10), arrowprops=dict(arrowstyle='<->'))
    ax.text(vis_f / 2, -25, f"f: {f_calc:.1f}mm", ha='center')

    # Final visual tweaks
    ax.set_xlim(-wd - 50, vis_f + 50)
    ax.set_ylim(-fov / 2 - 50, fov / 2 + 50)
    ax.axhline(0, color='black', lw=0.5, alpha=0.3)
    ax.set_axis_off()
    ax.legend(loc='upper left')


# UI Sliders
ax_wd = plt.axes([0.2, 0.18, 0.6, 0.03], facecolor='#ecf0f1')
ax_fov = plt.axes([0.2, 0.13, 0.6, 0.03], facecolor='#ecf0f1')
ax_sensor = plt.axes([0.2, 0.08, 0.6, 0.03], facecolor='#ecf0f1')

s_wd = Slider(ax_wd, 'WD (mm)', 100, 2000, valinit=500)
s_fov = Slider(ax_fov, 'FOV (mm)', 10, 1000, valinit=200)
s_sensor = Slider(ax_sensor, 'Sensor S (mm)', 3, 25, valinit=8)

s_wd.on_changed(update)
s_fov.on_changed(update)
s_sensor.on_changed(update)

update(None)
plt.show()