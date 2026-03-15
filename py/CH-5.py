import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation

def load_sample_image():
    img = cv2.imread('1.png', cv2.IMREAD_COLOR)
    if img is None:
        img = np.zeros((300, 400, 3), dtype=np.uint8)
        cv2.putText(img, 'Sample Image', (50, 150),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def create_hdr_effect(img, stops_range):
    hdr_img = np.zeros_like(img, dtype=np.float32)
    for i in range(3):
        channel = img[:,:,i].astype(np.float32) / 255.0
        hdr_channel = np.log1p(np.power(2, stops_range) * channel) / np.log1p(np.power(2, stops_range))
        hdr_img[:,:,i] = (hdr_channel * 255).clip(0, 255)
    return hdr_img.astype(np.uint8)

def simulate_dynamic_range(img, dynamic_range):
    low = 0 + (255 - dynamic_range) // 2
    high = 255 - (255 - dynamic_range) // 2
    limited_img = np.clip(img, low, high)
    normalized_img = ((limited_img - low) / (high - low) * 255).astype(np.uint8)
    return normalized_img

def update_dynamic_range(val):
    global current_dynamic_range
    current_dynamic_range = int(val)
    limited_img = simulate_dynamic_range(original_img, current_dynamic_range)
    img_plot.set_array(limited_img)
    ax1.set_title(f'Limited Dynamic Range: {current_dynamic_range}/255')
    fig.canvas.draw_idle()

def update_hdr_stops(val):
    global current_hdr_stops
    current_hdr_stops = val
    hdr_img = create_hdr_effect(original_img, current_hdr_stops)
    hdr_plot.set_array(hdr_img)
    ax2.set_title(f'HDR Effect: {current_hdr_stops:.1f} stops')
    fig.canvas.draw_idle()

def reset_parameters(event):
    dr_slider.set_val(128)
    hdr_slider.set_val(4.0)

original_img = load_sample_image()
current_dynamic_range = 128
current_hdr_stops = 4.0

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
plt.subplots_adjust(bottom=0.3)

img_plot = ax1.imshow(simulate_dynamic_range(original_img, current_dynamic_range))
ax1.set_title(f'Limited Dynamic Range: {current_dynamic_range}/255')
hdr_plot = ax2.imshow(create_hdr_effect(original_img, current_hdr_stops))
ax2.set_title(f'HDR Effect: {current_hdr_stops:.1f} stops')

ax_dr = plt.axes([0.2, 0.2, 0.6, 0.03])
ax_hdr = plt.axes([0.2, 0.15, 0.6, 0.03])
ax_reset = plt.axes([0.4, 0.05, 0.2, 0.05])

dr_slider = Slider(ax_dr, 'Dynamic Range', 10, 255, valinit=current_dynamic_range, valstep=1)
hdr_slider = Slider(ax_hdr, 'HDR Stops', 1.0, 8.0, valinit=current_hdr_stops, valstep=0.1)
reset_button = Button(ax_reset, 'Reset Parameters')

dr_slider.on_changed(update_dynamic_range)
hdr_slider.on_changed(update_hdr_stops)
reset_button.on_clicked(reset_parameters)

def animate_dr(i):
    val = 10 + (i % 246)
    dr_slider.set_val(val)

def animate_hdr(i):
    val = 1.0 + (i % 70) * 0.1
    hdr_slider.set_val(val)

ani_dr = FuncAnimation(fig, animate_dr, frames=246, interval=50, repeat=True)
ani_hdr = FuncAnimation(fig, animate_hdr, frames=70, interval=50, repeat=True)

plt.show()