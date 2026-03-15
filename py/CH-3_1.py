import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image

# --- Configuration ---
IMG_PATH = None  # You can put your image path here, e.g., "target.jpg"
SCENE_WIDTH = 400
SCENE_HEIGHT = 300
MOVE_SPEED = 2.0  # Pixels per row delay


def create_test_image():
    """Create a grid image if no user image is provided."""
    img = np.zeros((SCENE_HEIGHT, SCENE_WIDTH, 3), dtype=np.uint8) + 255
    # Draw a vertical bar
    img[:, 180:220, :] = [52, 152, 219]  # Blue bar
    # Draw horizontal grid lines
    for i in range(0, SCENE_HEIGHT, 50):
        img[i:i + 2, :, :] = 0
    return img


# Load and resize image
if IMG_PATH:
    try:
        raw_img = Image.open(IMG_PATH).convert('RGB')
        raw_img = raw_img.resize((SCENE_WIDTH, SCENE_HEIGHT))
        base_img = np.array(raw_img)
    except:
        base_img = create_test_image()
else:
    base_img = create_test_image()

fig = plt.figure(figsize=(14, 8), facecolor='#f0f0f0')
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], width_ratios=[1.2, 1])

ax_scene = fig.add_subplot(gs[0, 0])  # Live Scene
ax_timing = fig.add_subplot(gs[1, 0])  # Exposure Timing Diagram
ax_global = fig.add_subplot(gs[0, 1])  # Global Result
ax_rolling = fig.add_subplot(gs[1, 1])  # Rolling Result

# Pre-calculate Rolling Shutter Effect
rolling_img = np.zeros_like(base_img)
for y in range(SCENE_HEIGHT):
    shift = int(y * MOVE_SPEED)
    row = np.roll(base_img[y], shift, axis=0)
    rolling_img[y] = row


def init():
    ax_scene.set_title("LIVE SCENE (Fast Moving)", fontsize=10, fontweight='bold')
    ax_timing.set_title("EXPOSURE TIMING (Row vs Time)", fontsize=10, fontweight='bold')
    ax_global.set_title("GLOBAL SHUTTER RESULT", fontsize=10, fontweight='bold', color='#2980b9')
    ax_rolling.set_title("ROLLING SHUTTER RESULT", fontsize=10, fontweight='bold', color='#e67e22')

    for ax in [ax_scene, ax_global, ax_rolling]:
        ax.set_xticks([]);
        ax.set_yticks([])

    ax_timing.set_xlim(0, SCENE_WIDTH + SCENE_HEIGHT * MOVE_SPEED)
    ax_timing.set_ylim(SCENE_HEIGHT, 0)
    ax_timing.set_xlabel("Time (Horizontal Position)")
    ax_timing.set_ylabel("Sensor Row Index")
    return []


# Objects for animation
im_scene = ax_scene.imshow(base_img)
im_global = ax_global.imshow(np.zeros_like(base_img) + 255)
im_rolling = ax_rolling.imshow(np.zeros_like(base_img) + 255)
scan_line = ax_scene.axhline(y=0, color='red', lw=2, alpha=0)
timing_marker, = ax_timing.plot([], [], color='red', marker='o', markersize=4)


def animate(frame):
    # Live Scene Motion
    t = frame % 100
    shift = int(t * 5)
    current_scene = np.roll(base_img, shift, axis=1)
    im_scene.set_array(current_scene)

    # Trigger Snapshot every 100 frames
    if t < 60:  # Scanning phase
        scan_y = int((t / 60) * SCENE_HEIGHT)
        scan_line.set_ydata([scan_y, scan_y])
        scan_line.set_alpha(1)

        # Update Rolling Result row by row
        current_rolling = im_rolling.get_array().copy()
        current_rolling[scan_y] = rolling_img[scan_y]
        im_rolling.set_array(current_rolling)

        # Timing Diagram: Diagonal line for rolling
        ax_timing.plot([scan_y * MOVE_SPEED, (scan_y + 1) * MOVE_SPEED], [scan_y, scan_y], color='#e67e22', lw=2)

    if t == 1:  # Global Snapshot moment
        im_global.set_array(base_img)
        # Timing Diagram: Vertical line for global
        ax_timing.axvline(x=0, color='#2980b9', lw=4, alpha=0.5)

    if t == 90:  # Reset results for next cycle
        im_global.set_array(np.zeros_like(base_img) + 255)
        im_rolling.set_array(np.zeros_like(base_img) + 255)
        ax_timing.clear()
        init()
        scan_line.set_alpha(0)

    return im_scene, im_global, im_rolling, scan_line


ani = animation.FuncAnimation(fig, animate, frames=200, init_func=init, interval=30)
plt.show()