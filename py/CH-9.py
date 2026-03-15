import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.patches as patches

# 1. Setup Dashboard
fig = plt.figure(figsize=(14, 8), facecolor='#f4f7f9')
plt.subplots_adjust(left=0.1, bottom=0.25, right=0.9, top=0.9, wspace=0.3)

ax_normal = fig.add_subplot(121)  # Normal Lens View
ax_tele = fig.add_subplot(122)  # Telecentric Lens View


def update(val):
    z_pos = s_dist.val  # Object distance from lens (mm)
    obj_h = 40  # Physical height of the object (mm)
    f_len = 100  # Focal length for normal lens simulation

    # --- Logic: Normal Lens (Perspective) ---
    ax_normal.clear()
    ax_normal.set_title("NORMAL LENS\n(Perspective: Nearer = Larger)", fontsize=12, fontweight='bold', color='#e67e22')
    # Image size changes with distance: h' = h * f / (z - f)
    mag_normal = f_len / (z_pos - f_len) if z_pos > f_len else 1
    img_h_normal = obj_h * mag_normal

    # Draw Rays (Converging)
    ax_normal.plot([-z_pos, 0, 50], [obj_h / 2, 0, -img_h_normal / 2], color='gray', alpha=0.3, ls='--')
    ax_normal.plot([-z_pos, 0, 50], [-obj_h / 2, 0, img_h_normal / 2], color='gray', alpha=0.3, ls='--')
    # Draw Object & Sensor
    ax_normal.plot([-z_pos, -z_pos], [-obj_h / 2, obj_h / 2], color='black', lw=4, label='Object')
    ax_normal.plot([50, 50], [-img_h_normal / 2, img_h_normal / 2], color='#e67e22', lw=6, label='Image on Sensor')
    ax_normal.set_xlim(-550, 100);
    ax_normal.set_ylim(-60, 60)
    ax_normal.text(-z_pos, obj_h / 2 + 5, f"Pos: {z_pos}mm", ha='center')
    ax_normal.text(50, img_h_normal / 2 + 5, f"Size: {img_h_normal:.1f}", color='#e67e22', fontweight='bold',
                   ha='center')

    # --- Logic: Telecentric Lens (Parallel) ---
    ax_tele.clear()
    ax_tele.set_title("TELECENTRIC LENS\n(Constant Magnification)", fontsize=12, fontweight='bold', color='#2ecc71')
    # Image size is constant: h' = h * Mag_fixed
    mag_fixed = 0.5
    img_h_tele = obj_h * mag_fixed

    # Draw Rays (Parallel to Axis)
    ax_tele.plot([-z_pos, 0, 0, 50], [obj_h / 2, obj_h / 2, 0, -img_h_tele / 2], color='gray', alpha=0.3, ls='--')
    ax_tele.plot([-z_pos, 0, 0, 50], [-obj_h / 2, -obj_h / 2, 0, img_h_tele / 2], color='gray', alpha=0.3, ls='--')
    # Draw Object & Sensor
    ax_tele.plot([-z_pos, -z_pos], [-obj_h / 2, obj_h / 2], color='black', lw=4)
    ax_tele.plot([50, 50], [-img_h_tele / 2, img_h_tele / 2], color='#2ecc71', lw=6)
    ax_tele.set_xlim(-550, 100);
    ax_tele.set_ylim(-60, 60)
    ax_tele.text(50, img_h_tele / 2 + 5, f"Size: {img_h_tele:.1f} (Fixed)", color='#27ae60', fontweight='bold',
                 ha='center')

    fig.canvas.draw_idle()


# --- Slider ---
s_dist = Slider(plt.axes([0.2, 0.1, 0.6, 0.04], facecolor='#dfe6e9'), 'Object Distance', 150, 500, valinit=300)
s_dist.on_changed(update)

update(None)
plt.show()