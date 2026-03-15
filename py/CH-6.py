import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.patches as patches

# 1. Setup Figure
fig, ax = plt.subplots(figsize=(12, 8), facecolor='#f8f9fa')
plt.subplots_adjust(left=0.1, bottom=0.25, right=0.9, top=0.9)

# Define Interface Zones (Name, Distance_Limit, Bandwidth_Limit, Color)
interfaces = [
    {"name": "USB 3.0", "dist": 5, "bw": 400, "color": "#3498db", "alpha": 0.3},
    {"name": "GigE Vision", "dist": 100, "bw": 100, "color": "#2ecc71", "alpha": 0.3},
    {"name": "Camera Link (Full)", "dist": 10, "bw": 850, "color": "#f1c40f", "alpha": 0.3},
    {"name": "CoaXPress (CXP-12)", "dist": 150, "bw": 1250, "color": "#e74c3c", "alpha": 0.3},
]


def update(val):
    req_dist = s_dist.val
    req_bw = s_bw.val

    ax.clear()
    ax.set_title("CAMERA INTERFACE SELECTION GUIDE", fontsize=14, fontweight='bold')
    ax.set_xlabel("Transmission Distance (Meters)")
    ax.set_ylabel("Required Bandwidth (MB/s)")

    # Draw interface "Territories"
    for i in interfaces:
        rect = patches.Rectangle((0, 0), i['dist'], i['bw'],
                                 linewidth=2, edgecolor=i['color'], facecolor=i['color'],
                                 alpha=i['alpha'], label=i['name'])
        ax.add_patch(rect)
        # Label the zones
        ax.text(i['dist'] * 0.7, i['bw'] * 0.9, i['name'], color=i['color'], fontweight='bold', ha='right')

    # Draw User Requirement Point
    ax.scatter(req_dist, req_bw, color='black', s=100, zorder=5, label='Your Requirement')
    ax.axhline(req_bw, color='black', lw=0.5, ls='--')
    ax.axvline(req_dist, color='black', lw=0.5, ls='--')

    # Selection Logic
    recommendation = "No Interface Fits"
    cost_info = ""

    # Check candidates (Simplification: find the most cost-effective one that fits)
    fit_found = False
    if req_dist <= 5 and req_bw <= 400:
        recommendation = "USB 3.0 (Best Value)"
        cost_info = "Cost: Low | CPU: Low | Setup: Easy"
        fit_found = True
    elif req_dist <= 100 and req_bw <= 100:
        recommendation = "GigE Vision (Long Range)"
        cost_info = "Cost: Lowest | CPU: High | Setup: Simple"
        fit_found = True
    elif req_dist <= 10 and req_bw <= 850:
        recommendation = "Camera Link (High Speed)"
        cost_info = "Cost: High | CPU: Low | Setup: Complex (Grabber Required)"
        fit_found = True
    elif req_dist <= 150 and req_bw <= 1250:
        recommendation = "CoaXPress (Ultimate Performance)"
        cost_info = "Cost: Highest | CPU: Low | Setup: Professional"
        fit_found = True

    ax.text(75, 1400, f"Recommendation: {recommendation}", fontsize=12,
            bbox=dict(facecolor='white', alpha=0.8), ha='center', fontweight='bold')
    ax.text(75, 1320, cost_info, fontsize=10, ha='center', color='gray')

    ax.set_xlim(0, 160)
    ax.set_ylim(0, 1500)
    ax.grid(True, linestyle=':', alpha=0.6)


# UI Sliders
ax_dist_s = plt.axes([0.2, 0.12, 0.6, 0.03], facecolor='#ecf0f1')
ax_bw_s = plt.axes([0.2, 0.07, 0.6, 0.03], facecolor='#ecf0f1')

s_dist = Slider(ax_dist_s, 'Distance (m)', 0, 150, valinit=30)
s_bw = Slider(ax_bw_s, 'Bandwidth (MB/s)', 0, 1400, valinit=200)

s_dist.on_changed(update)
s_bw.on_changed(update)

update(None)
plt.show()