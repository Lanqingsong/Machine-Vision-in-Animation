import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# Function to generate a synthetic 3D scene with varying focus
def generate_3d_scene(image_size=(400, 400), focus_distance_norm=0.5, current_f_stop=4.0):
    # Base image for the scene
    scene_base_img = Image.new('L', image_size, color=255)  # Start with white background

    # Simulate font for text, adjust if not found
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
        # print("Arial font not found, using default. Text size might vary.")

    # Simulate foreground (close), midground (focus), background (far) objects
    # z_pos_norm: normalized distance from camera (0=very close, 1=very far)
    objects = [
        {"text": "Foreground", "z_pos_norm": 0.2, "color": 150, "coords": (50, 50)},
        {"text": "Midground", "z_pos_norm": 0.5, "color": 100, "coords": (50, 180)},
        {"text": "Background", "z_pos_norm": 0.8, "color": 50, "coords": (50, 310)}
    ]

    # Simulate Depth of Field blur
    # Larger f_stop (smaller aperture) -> less blur (deeper DoF)
    # Smaller f_stop (larger aperture) -> more blur (shallower DoF)

    # Heuristic for blur radius: smaller F-number, larger blur_scale;
    # blur also increases with distance from the focal plane.
    # The '100' here is an arbitrary scaling factor for visual effect.
    blur_scale_factor = 100 / current_f_stop

    # Composite all objects with appropriate blur
    final_scene_img = Image.new('L', image_size, color=255)  # Start with white for compositing

    for obj in objects:
        text_img_layer = Image.new('L', image_size, color=255)  # Transparent layer for each text
        text_draw = ImageDraw.Draw(text_img_layer)
        text_draw.text(obj["coords"], obj["text"], font=font, fill=obj["color"])

        # Calculate blur radius based on z_pos and f_stop
        distance_from_focus_plane = abs(obj["z_pos_norm"] - focus_distance_norm)
        blur_radius = int(distance_from_focus_plane * blur_scale_factor)

        # Apply blur if radius > 0
        if blur_radius > 0:
            # Clamp blur_radius to prevent extremely large blurs that are slow/unrealistic
            blurred_text_img_layer = text_img_layer.filter(
                ImageFilter.GaussianBlur(radius=min(blur_radius, 10)))  # Max blur 10px
            final_scene_img = Image.composite(blurred_text_img_layer, final_scene_img,
                                              blurred_text_img_layer)  # Composite by darkening
        else:
            final_scene_img = Image.composite(text_img_layer, final_scene_img, text_img_layer)  # Composite sharp text

    # Simulate brightness based on f_stop (larger F-number, darker)
    # This is a simplified visual representation, not photometrically accurate.
    # We apply brightness adjustment to the final composited scene.
    brightness_factor = (initial_f_stop / current_f_stop) ** 2  # Inverse square law for light

    # Convert to NumPy array for brightness adjustment
    scene_np = np.array(final_scene_img, dtype=np.float32)
    scene_np = np.clip(scene_np * brightness_factor, 0, 255)  # Apply brightness and clip

    return scene_np.astype(np.uint8)


# --- Setup Plot ---
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(left=0.1, bottom=0.25)

# Initial parameters
initial_f_stop = 4.0
focus_distance_norm = 0.5  # Midground is in focus

# Generate initial scene
initial_scene = generate_3d_scene(focus_distance_norm=focus_distance_norm, current_f_stop=initial_f_stop)
img_display = ax.imshow(initial_scene, cmap='gray', vmin=0, vmax=255)
ax.set_title(f'Scene (F/{initial_f_stop:.1f})')
ax.set_xticks([]);
ax.set_yticks([])

# --- Slider for F-stop ---
ax_fstop = plt.axes([0.15, 0.1, 0.7, 0.03])
# Removed readout=True and valfmt='F/%.1f' for broader compatibility
fstop_slider = Slider(ax_fstop, 'Aperture (F-stop)', 1.4, 22.0, valinit=initial_f_stop, valstep=0.1)


# --- Update Function ---
def update(val):
    current_f_stop = fstop_slider.val

    new_scene = generate_3d_scene(focus_distance_norm=focus_distance_norm, current_f_stop=current_f_stop)
    img_display.set_data(new_scene)
    ax.set_title(f'Scene (F/{current_f_stop:.1f})')
    fig.canvas.draw_idle()


fstop_slider.on_changed(update)

update(None)  # Initial call to set everything up

plt.show()