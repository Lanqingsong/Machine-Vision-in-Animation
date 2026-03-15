import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import matplotlib.patches as patches

# 1. Setup Dashboard
fig = plt.figure(figsize=(12, 8), facecolor='#fdfdfd')
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)

ax_mech = fig.add_subplot(121)  # Mechanical Cross-section
ax_view = fig.add_subplot(122)  # Simulated View


def update(label):
    # Get current selections
    l_type = rad_lens.value_selected
    c_type = rad_cam.value_selected
    has_spacer = rad_spacer.value_selected == "5mm Spacer ON"

    # Define Flange Focal Distances (FFD)
    ffd_c = 17.526
    ffd_cs = 12.526

    # Determine Physical Setup
    lens_needs = ffd_c if l_type == "C-Mount Lens" else ffd_cs
    cam_provides = ffd_c if c_type == "C-Mount Camera" else ffd_cs
    actual_dist = cam_provides + (5.0 if has_spacer else 0.0)

    # Calculate Blur
    focus_error = abs(actual_dist - lens_needs)
    is_clear = focus_error < 0.1

    # --- 1. Draw Mechanical View ---
    ax_mech.clear()
    ax_mech.set_title("MECHANICAL: Flange Focal Distance", fontsize=12, fontweight='bold')

    # Draw Camera Body (Sensor is at x=0)
    ax_mech.add_patch(patches.Rectangle((-2, -20), 2, 40, color='gray', alpha=0.3))  # Sensor layer
    ax_mech.text(-1, 22, "Sensor", ha='center', color='red', fontweight='bold')
    ax_mech.axvline(0, color='red', lw=2)

    # Draw Camera Mount Face
    mount_x = cam_provides
    ax_mech.add_patch(patches.Rectangle((mount_x, -25), 3, 50, color='#2c3e50'))
    ax_mech.text(mount_x + 1.5, 27, f"{c_type}\n({cam_provides}mm)", ha='center', fontsize=9)

    # Draw Spacer if active
    spacer_offset = 0
    if has_spacer:
        ax_mech.add_patch(patches.Rectangle((mount_x + 3, -15), 5, 30, color='#f1c40f', alpha=0.8))
        ax_mech.text(mount_x + 5.5, -20, "+5mm Adapter", color='#d35400', fontweight='bold', ha='center')
        spacer_offset = 5

    # Draw Lens Rear (Threads)
    lens_x = mount_x + 3 + spacer_offset
    lens_color = '#3498db' if l_type == "C-Mount Lens" else '#e67e22'
    ax_mech.add_patch(patches.Rectangle((lens_x, -15), 20, 30, color=lens_color, alpha=0.7))
    ax_mech.text(lens_x + 10, 0, f"{l_type}\nNeeds {lens_needs}mm", ha='center', color='white', fontweight='bold')

    # Draw Light Rays
    if is_clear:
        ax_mech.plot([lens_x, 0, lens_x], [10, 0, -10], color='green', lw=2, label='Perfect Focus')
    else:
        # Rays converge at the wrong spot
        focus_spot = actual_dist - lens_needs
        ax_mech.plot([lens_x, -focus_spot, lens_x], [10, 0, -10], color='orange', ls='--', alpha=0.6,
                     label='Misaligned')

    ax_mech.set_xlim(-5, 40);
    ax_mech.set_ylim(-35, 35)
    ax_mech.set_axis_off()
    ax_mech.legend(loc='lower right')

    # --- 2. Draw Simulated View ---
    ax_view.clear()
    ax_view.set_title("RESULT: Image Sharpness", fontsize=12, fontweight='bold')
    if is_clear:
        ax_view.text(0.5, 0.5, "CLEAR ✓", fontsize=30, color='green', ha='center', va='center')
        ax_view.set_facecolor('#e8f5e9')
    else:
        status = "OUT OF FOCUS"
        if actual_dist > lens_needs:
            status += "\n(Lens too far)"
        else:
            status += "\n(Lens too close)"
        ax_view.text(0.5, 0.5, status, fontsize=20, color='red', ha='center', va='center', alpha=0.6)
        ax_view.set_facecolor('#ffebee')
    ax_view.set_xticks([]);
    ax_view.set_yticks([])

    fig.canvas.draw_idle()


# --- UI Controls ---
ax_rad_l = plt.axes([0.1, 0.15, 0.2, 0.1], facecolor='#f0f0f0')
rad_lens = RadioButtons(ax_rad_l, ("C-Mount Lens", "CS-Mount Lens"))

ax_rad_c = plt.axes([0.4, 0.15, 0.2, 0.1], facecolor='#f0f0f0')
rad_cam = RadioButtons(ax_rad_c, ("C-Mount Camera", "CS-Mount Camera"))

ax_rad_s = plt.axes([0.7, 0.15, 0.2, 0.1], facecolor='#f0f0f0')
rad_spacer = RadioButtons(ax_rad_s, ("No Spacer", "5mm Spacer ON"))

rad_lens.on_clicked(update)
rad_cam.on_clicked(update)
rad_spacer.on_clicked(update)

update(None)
plt.show()