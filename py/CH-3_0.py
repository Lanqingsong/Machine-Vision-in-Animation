import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

# 1. Setup Figure
fig = plt.figure(figsize=(12, 7), facecolor='#f8f9fa')
plt.subplots_adjust(top=0.85, bottom=0.15)

# Subplot 1: Global Shutter (All pixels at once)
ax_global = fig.add_subplot(121)
# Subplot 2: Rolling Shutter (Line by line)
ax_rolling = fig.add_subplot(122)

# Parameters
object_speed = 0.5  # mm per time step
frame_height = 100
frame_width = 100
object_width = 10


def init():
    ax_global.set_title("GLOBAL SHUTTER\n(Simultaneous Exposure)", fontsize=12, fontweight='bold', color='#2980b9')
    ax_rolling.set_title("ROLLING SHUTTER\n(Line-by-Line Exposure)", fontsize=12, fontweight='bold', color='#e67e22')
    for ax in [ax_global, ax_rolling]:
        ax.set_xlim(0, frame_width)
        ax.set_ylim(0, frame_height)
        ax.set_aspect('equal')
        # Draw a scanning line placeholder
        ax.scan_line = ax.axhline(y=frame_height, color='red', lw=1, ls='--', alpha=0)
    return []


def animate(frame):
    # 'frame' acts as the time sequence
    # Current horizontal position of the moving object
    current_x = (frame * object_speed) % frame_width

    # --- Global Shutter Logic ---
    ax_global.clear()
    init()
    # At the moment of capture, all pixels see the object at current_x
    # We simulate a "Flash" capture at specific intervals
    capture_trigger = (frame // 20) * 20  # Trigger every 20 steps
    fixed_x = (capture_trigger * object_speed) % frame_width

    rect_g = patches.Rectangle((fixed_x, 10), object_width, 80, color='#3498db', alpha=0.8)
    ax_global.add_patch(rect_g)
    ax_global.text(5, 5, "Captured Shape: Straight", color='#2980b9', fontsize=10)

    # --- Rolling Shutter Logic ---
    ax_rolling.clear()
    init()
    # Rolling shutter captures row 'y' at time 't'
    # The scan line moves from top (y=100) to bottom (y=0)
    scan_y = frame % frame_height

    # We redraw the "Skewed" shape based on time delay per row
    # Each row y was captured at a different time (and thus different x position)
    scan_line_pos = 100 - scan_y
    ax_rolling.axhline(y=scan_line_pos, color='red', lw=2, label='Scan Line')

    # Calculate skewed vertices
    # Top of object captured earlier, bottom captured later
    skew_pts = []
    for y in range(10, 90, 2):
        # Time delay logic: lower rows are captured later
        row_time_delay = (90 - y) / 2  # Simple delay model
        x_at_that_time = (fixed_x + row_time_delay * object_speed * 5) % frame_width
        row_rect = patches.Rectangle((x_at_that_time, y), object_width, 2, color='#e67e22', alpha=0.6)
        ax_rolling.add_patch(row_rect)

    ax_rolling.text(5, 5, "Captured Shape: Skewed!", color='#d35400', fontsize=10, fontweight='bold')

    return []


ani = animation.FuncAnimation(fig, animate, frames=200, init_func=init, blit=False, interval=50)
plt.show()