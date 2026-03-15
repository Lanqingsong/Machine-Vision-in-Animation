import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
from PIL import Image


def generate_complex_hdr_scene(width=256, height=256):
    x = np.linspace(-1.5, 1.5, width)
    y = np.linspace(-1.5, 1.5, height)
    X, Y = np.meshgrid(x, y)

    light_source = np.exp(-(X ** 2 + Y ** 2) / 0.3) * 10

    texture_R = (np.sin(X * 15) + np.cos(Y * 10) + 2) / 4 * 0.5
    texture_G = (np.cos(X * 12) + np.sin(Y * 18) + 2) / 4 * 0.7
    texture_B = (np.sin(X * 20) + np.cos(Y * 15) + 2) / 4 * 0.9

    hdr_R = light_source * (1.0 + texture_R * 0.5) + texture_R * 0.2
    hdr_G = light_source * (0.8 + texture_G * 0.7) + texture_G * 0.3
    hdr_B = light_source * (0.6 + texture_B * 0.9) + texture_B * 0.4

    hdr_R = np.clip(hdr_R, 0.001, 30)
    hdr_G = np.clip(hdr_G, 0.001, 30)
    hdr_B = np.clip(hdr_B, 0.001, 30)

    hdr_data = np.stack([hdr_R, hdr_G, hdr_B], axis=-1)

    return hdr_data


def calculate_luminance(rgb_image):
    return 0.2126 * rgb_image[..., 0] + 0.7152 * rgb_image[..., 1] + 0.0722 * rgb_image[..., 2]


def linear_tone_mapping(img, display_max_luminance=1.0):
    luminance = calculate_luminance(img)
    max_lum = np.max(luminance)

    if max_lum == 0:
        return np.zeros_like(img)

    return np.clip(img / max_lum * display_max_luminance, 0, 1)


def gamma_correction(img, gamma=2.2):
    normalized_img = img / np.max(img) if np.max(img) > 0 else np.zeros_like(img)
    return np.power(normalized_img, 1 / gamma)


def reinhard_tone_mapping(img, key=0.18, L_white=1.0):
    luminance = calculate_luminance(img)

    L_avg = np.exp(np.mean(np.log(luminance + 1e-6)))

    scaled_luminance = (luminance * key) / L_avg

    tone_mapped_luminance = scaled_luminance * (1 + scaled_luminance / (L_white ** 2)) / (1 + scaled_luminance)

    color_ratio = np.divide(img, luminance[..., np.newaxis], out=np.zeros_like(img),
                            where=luminance[..., np.newaxis] != 0)

    tone_mapped_img = color_ratio * tone_mapped_luminance[..., np.newaxis]

    return np.clip(tone_mapped_img, 0, 1)


hdr_image_rgb = generate_complex_hdr_scene()

current_tone_mapper = 'Reinhard'
initial_gamma = 2.2
initial_reinhard_key = 0.18
initial_reinhard_lwhite = 1.0

fig, (ax_img, ax_hist) = plt.subplots(1, 2, figsize=(12, 6), gridspec_kw={'width_ratios': [3, 1]})
plt.subplots_adjust(left=0.08, bottom=0.35, right=0.95, wspace=0.3)

tone_mapped_img = reinhard_tone_mapping(hdr_image_rgb, initial_reinhard_key, initial_reinhard_lwhite)
img_display = ax_img.imshow(tone_mapped_img, aspect='auto')
ax_img.set_title(f'Tone Mapped Image ({current_tone_mapper})')
ax_img.set_xticks([])
ax_img.set_yticks([])

hdr_luminance = calculate_luminance(hdr_image_rgb)
hist_bins = np.linspace(0, 1, 64)
hdr_hist_bins = np.logspace(-3, np.log10(np.max(hdr_luminance)), 64)
hist_alpha = 0.6

ax_hist.set_xscale('log')
ax_hist.set_title('Luminance Histogram')
ax_hist.set_xlabel('Luminance (log scale)')
ax_hist.set_ylabel('Pixel Count')
hdr_hist_values, _ = np.histogram(hdr_luminance.flatten(), bins=hdr_hist_bins)
hdr_hist_plot = ax_hist.plot(hdr_hist_bins[:-1], hdr_hist_values, color='gray', linestyle='--', label='Original HDR')

ldr_luminance_initial = calculate_luminance(tone_mapped_img)
ldr_hist_plot = ax_hist.hist(ldr_luminance_initial.flatten(), bins=hist_bins, color='blue', alpha=hist_alpha,
                             label='Tone Mapped LDR')
ax_hist.legend()
ax_hist.set_ylim(bottom=0)

rax = plt.axes([0.02, 0.7, 0.15, 0.2])
radio = RadioButtons(rax, ('Linear', 'Gamma', 'Reinhard'))

ax_gamma = plt.axes([0.2, 0.2, 0.7, 0.03])
gamma_slider = Slider(ax_gamma, 'Gamma', 0.5, 4.0, valinit=initial_gamma, valstep=0.1)

ax_reinhard_key = plt.axes([0.2, 0.15, 0.7, 0.03])
reinhard_key_slider = Slider(ax_reinhard_key, 'Reinhard Key', 0.05, 0.5, valinit=initial_reinhard_key, valstep=0.01)

ax_reinhard_lwhite = plt.axes([0.2, 0.1, 0.7, 0.03])
reinhard_lwhite_slider = Slider(ax_reinhard_lwhite, 'Reinhard L_white', 0.5, 5.0, valinit=initial_reinhard_lwhite,
                                valstep=0.1)

# Set initial slider active states based on current_tone_mapper
gamma_slider.set_active(current_tone_mapper == 'Gamma')
reinhard_key_slider.set_active(current_tone_mapper == 'Reinhard')
reinhard_lwhite_slider.set_active(current_tone_mapper == 'Reinhard')


def update_image(val=None):
    global current_tone_mapper

    if current_tone_mapper == 'Linear':
        new_image = linear_tone_mapping(hdr_image_rgb)
    elif current_tone_mapper == 'Gamma':
        new_image = gamma_correction(hdr_image_rgb, gamma_slider.val)
    elif current_tone_mapper == 'Reinhard':
        new_image = reinhard_tone_mapping(hdr_image_rgb, reinhard_key_slider.val, reinhard_lwhite_slider.val)

    img_display.set_data(new_image)
    ax_img.set_title(f'Tone Mapped Image ({current_tone_mapper})')

    ldr_luminance = calculate_luminance(new_image)
    ax_hist.clear()
    ax_hist.set_xscale('log')
    ax_hist.set_title('Luminance Histogram')
    ax_hist.set_xlabel('Luminance (log scale)')
    ax_hist.set_ylabel('Pixel Count')
    ax_hist.plot(hdr_hist_bins[:-1], hdr_hist_values, color='gray', linestyle='--', label='Original HDR')
    ax_hist.hist(ldr_luminance.flatten(), bins=hist_bins, color='blue', alpha=hist_alpha, label='Tone Mapped LDR')
    ax_hist.legend()
    ax_hist.set_ylim(bottom=0)

    fig.canvas.draw_idle()


def tone_mapper_selection(label):
    global current_tone_mapper
    current_tone_mapper = label

    # Correctly set active state for all sliders
    gamma_slider.set_active(label == 'Gamma')
    reinhard_key_slider.set_active(label == 'Reinhard')
    reinhard_lwhite_slider.set_active(label == 'Reinhard')

    update_image()


radio.on_clicked(tone_mapper_selection)
gamma_slider.on_changed(update_image)
reinhard_key_slider.on_changed(update_image)
reinhard_lwhite_slider.on_changed(update_image)

update_image()

plt.show()