import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.patches as patches
import numpy as np

# 1. Setup Dashboard
fig = plt.figure(figsize=(14, 8), facecolor='#fdfdfd')
plt.subplots_adjust(left=0.1, bottom=0.3, right=0.9, top=0.9, wspace=0.3)

ax_optics = fig.add_subplot(121)  # Side view of lens and DoF
ax_view = fig.add_subplot(122)  # Perspective view of object depth


def update(val):
    f_len = s_f.val  # Focal length (mm)
    f_stop = s_stop.val  # F-number (Aperture)
    dist = s_dist.val  # Focus distance (mm)

    # --- Accurate DoF Calculation (Thin Lens Formula) ---
    # COC (Circle of Confusion): typical 0.03mm for industrial vision
    coc = 0.03
    # Standard asymmetric DoF formula:
    #   Near limit = f^2 * s / (f^2 + N * c * (s - f))
    #   Far  limit = f^2 * s / (f^2 - N * c * (s - f))
    # DoF is NOT symmetric: far side is always deeper than near side
    denom_common = f_stop * coc * (dist - f_len)
    near_limit = (f_len ** 2 * dist) / (f_len ** 2 + denom_common)
    # Guard: if denominator <= 0, object is inside hyperfocal -> far limit = infinity
    denom_far = f_len ** 2 - denom_common
    far_limit = (f_len ** 2 * dist) / denom_far if denom_far > 0 else float('inf')
    far_limit = min(far_limit, dist + 2000)  # Cap for display purposes

    # --- 1. Update Optics Side View ---
    ax_optics.clear()
    ax_optics.set_title("OPTICS: Light Cone & DoF Zone", fontsize=12, fontweight='bold')

    # Draw Lens
    lens = patches.Ellipse((0, 0), 20, 60 / f_stop + 10, color='#3498db', alpha=0.6)
    ax_optics.add_patch(lens)
    ax_optics.text(-5, 40, f"Aperture: f/{f_stop:.1f}", ha='center')

    # Draw Focus Plane & DoF Zone
    ax_optics.axvline(dist, color='red', lw=2, label='Focus Plane')
    dof_rect = patches.Rectangle((near_limit, -50), far_limit - near_limit, 100,
                                 color='green', alpha=0.2, label='Depth of Field')
    ax_optics.add_patch(dof_rect)

    # Draw Light Rays (Cones)
    # Converging to focus point
    ax_optics.plot([0, dist, 0], [30 / f_stop, 0, -30 / f_stop], color='orange', alpha=0.6, ls='--')
    # Diverging after focus
    ax_optics.plot([dist, dist + 100], [0, 20 / f_stop], color='orange', alpha=0.3, ls='--')
    ax_optics.plot([dist, dist + 100], [0, -20 / f_stop], color='orange', alpha=0.3, ls='--')

    ax_optics.set_xlim(-50, 600)
    ax_optics.set_ylim(-60, 60)
    ax_optics.set_xlabel("Distance (mm)")
    ax_optics.legend(loc='upper right')

    # --- 2. Update Perspective Object View ---
    ax_view.clear()
    ax_view.set_title("OBJECT: Thickness / Depth Inspection", fontsize=12, fontweight='bold')

    # We simulate an object with thickness (a tilted slope)
    z_depths = np.linspace(100, 500, 20)
    for z in z_depths:
        # Determine sharpness based on distance to DoF
        if near_limit <= z <= far_limit:
            color = 'green'
            marker_size = 15
            label = "Sharp"
        else:
            color = 'gray'
            # Further from DoF = smaller/blurrier representation
            marker_size = 10 / (1 + abs(z - dist) / 50)
            label = "Blurry"

        ax_view.scatter(z, 0, s=marker_size * 10, color=color, alpha=0.6)

    ax_view.axvspan(near_limit, far_limit, color='green', alpha=0.1)
    ax_view.set_xlim(50, 550)
    ax_view.set_yticks([])
    ax_view.set_xlabel("Depth Position (mm)")
    ax_view.text(dist, 0.1, "Target", color='red', ha='center', fontweight='bold')

    fig.canvas.draw_idle()


# --- Sliders ---
ax_color = '#ecf0f1'
s_f = Slider(plt.axes([0.2, 0.18, 0.6, 0.03], facecolor=ax_color), 'Focal Length (f)', 8, 100, valinit=25)
s_stop = Slider(plt.axes([0.2, 0.13, 0.6, 0.03], facecolor=ax_color), 'F-Stop (Aperture)', 1.4, 16, valinit=4.0)
s_dist = Slider(plt.axes([0.2, 0.08, 0.6, 0.03], facecolor=ax_color), 'Distance (s)', 100, 500, valinit=300)

s_f.on_changed(update)
s_stop.on_changed(update)
s_dist.on_changed(update)

update(None)
plt.show()
