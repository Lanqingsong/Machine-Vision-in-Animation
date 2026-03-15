import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

fig = plt.figure(figsize=(12, 6), facecolor='#f8f9fa')
plt.subplots_adjust(left=0.1, bottom=0.25, right=0.95, top=0.9, wspace=0.3)

ax_ray = fig.add_subplot(121)
ax_mag = fig.add_subplot(122)

x_obj = -50
x_lens = 0
x_sensor = 50
y_obj = np.array([10, 20, 30, 40])


def draw_physics(k):
    ax_ray.clear()
    ax_mag.clear()

    ax_ray.axhline(0, color='black', ls='-.', alpha=0.3)
    ax_ray.axvline(x_lens, color='#3498db', lw=8, alpha=0.5, label='Spherical Lens')
    ax_ray.axvline(x_sensor, color='#2c3e50', lw=4, label='Sensor Plane')

    ax_ray.plot(x_obj, 0, 'ko')
    ax_ray.text(x_obj, -5, 'Optical Axis', ha='center')

    for y in y_obj:
        y_ideal = -y
        y_real = -y * (1 + k * (y / 40) ** 2)

        ax_ray.plot([x_obj, x_lens, x_sensor], [y, 0, y_ideal], color='#2ecc71', ls='--', lw=1.5, alpha=0.6)

        ax_ray.plot([x_obj, x_lens], [y, y * 0.5], color='#e74c3c', ls='-', lw=1.5, alpha=0.8)
        ax_ray.plot([x_lens, x_sensor], [y * 0.5, y_real], color='#e74c3c', ls='-', lw=1.5, alpha=0.8)

        ax_ray.plot(x_obj, y, 'ro', markersize=4)
        ax_ray.plot(x_sensor, y_real, 'ro', markersize=4)

    ax_ray.plot([], [], color='#2ecc71', ls='--', label='Ideal Paraxial Ray')
    ax_ray.plot([], [], color='#e74c3c', ls='-', label='Real Marginal Ray')

    ax_ray.set_title("Physics Cause: Ray Deviation", fontweight='bold')
    ax_ray.set_xlim(-60, 60)
    ax_ray.set_ylim(-60, 60)
    ax_ray.legend(loc='lower left')
    ax_ray.axis('off')

    r = np.linspace(0, 40, 100)
    mag_ideal = np.ones_like(r)
    mag_real = 1 * (1 + k * (r / 40) ** 2)

    ax_mag.plot(r, mag_ideal, color='#2ecc71', ls='--', lw=2, label='Ideal Lens (Constant Mag)')
    ax_mag.plot(r, mag_real, color='#e74c3c', ls='-', lw=2, label='Real Lens (Variable Mag)')

    ax_mag.fill_between(r, mag_ideal, mag_real, color='#e74c3c', alpha=0.1)

    ax_mag.set_title("Core Essence: Magnification vs. Radius", fontweight='bold')
    ax_mag.set_xlabel("Radial Distance from Center (r)")
    ax_mag.set_ylabel("Transverse Magnification (M)")
    ax_mag.set_ylim(0.5, 1.5)
    ax_mag.grid(True, linestyle=':', alpha=0.6)
    ax_mag.legend()


ax_k = plt.axes([0.2, 0.1, 0.6, 0.04], facecolor='#ecf0f1')
s_k = Slider(ax_k, 'Lens Spherical Error (k)', -0.4, 0.4, valinit=0)


def update(val):
    draw_physics(s_k.val)
    fig.canvas.draw_idle()


s_k.on_changed(update)
draw_physics(0)
plt.show()