import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.patches as patches
import numpy as np

# --- 1. 初始化窗口 ---
fig = plt.figure(figsize=(12, 8), facecolor='#f5f6fa')
fig.canvas.manager.set_window_title('Normal vs Telecentric Lens')
plt.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=0.9, wspace=0.3, hspace=0.3)

# 创建4个子图 (2x2)
ax_norm_side = fig.add_subplot(221)
ax_tele_side = fig.add_subplot(222)
ax_norm_cam = fig.add_subplot(223)
ax_tele_cam = fig.add_subplot(224)

# 物体参数 (一个具有厚度的圆柱体/深孔)
obj_radius = 20
obj_thickness = 40
focal_length = 50


def update(val):
    z_dist = s_dist.val  # 物体距离镜头的距离

    # 清空画布
    for ax in [ax_norm_side, ax_tele_side, ax_norm_cam, ax_tele_cam]:
        ax.clear()

    # ==========================================
    # 上半部分：光路侧视图 (Side View)
    # ==========================================
    for ax, title in zip([ax_norm_side, ax_tele_side], ['Normal Lens (Ray Tracing)', 'Telecentric Lens (Ray Tracing)']):
        ax.set_title(title, fontweight='bold')
        ax.set_xlim(-10, 200)
        ax.set_ylim(-40, 40)
        ax.axhline(0, color='gray', linestyle='-.', alpha=0.5)  # 光轴
        # 镜头示意
        ax.add_patch(patches.Ellipse((0, 0), 10, 60, color='#3498db', alpha=0.5))

        # 画物体 (侧面看是一个矩形)
        rect = patches.Rectangle((z_dist, -obj_radius), obj_thickness, obj_radius * 2,
                                 edgecolor='black', facecolor='#e74c3c', alpha=0.6)
        ax.add_patch(rect)

    # 普通镜头光路 (向中心汇聚)
    ax_norm_side.plot([z_dist, 0], [obj_radius, 0], 'r--', alpha=0.7)
    ax_norm_side.plot([z_dist, 0], [-obj_radius, 0], 'r--', alpha=0.7)
    ax_norm_side.plot([z_dist + obj_thickness, 0], [obj_radius, 0], 'b--', alpha=0.7)

    # 远心镜头光路 (平行光进入)
    ax_tele_side.plot([z_dist, 0], [obj_radius, obj_radius], 'r--', alpha=0.7)
    ax_tele_side.plot([z_dist, 0], [-obj_radius, -obj_radius], 'r--', alpha=0.7)
    ax_tele_side.plot([z_dist + obj_thickness, 0], [obj_radius, obj_radius], 'b--', alpha=0.7)

    # ==========================================
    # 下半部分：相机成像视图 (Camera View)
    # ==========================================
    # 计算普通镜头的透视放大率 (近大远小)
    mag_top = focal_length / z_dist
    mag_bot = focal_length / (z_dist + obj_thickness)

    # 远心镜头的放大率是恒定的
    mag_tele = 0.5

    for ax, title in zip([ax_norm_cam, ax_tele_cam], ['Normal Lens Camera View', 'Telecentric Lens Camera View']):
        ax.set_title(title, fontweight='bold')
        ax.set_xlim(-30, 30)
        ax.set_ylim(-30, 30)
        ax.set_aspect('equal')
        ax.axis('off')
        # 传感器背景
        ax.add_patch(patches.Rectangle((-30, -30), 60, 60, color='#2c3e50'))

    # 普通镜头画面：看到顶部大圆，和底部小圆，以及它们之间的"侧壁"
    top_r_norm = obj_radius * mag_top
    bot_r_norm = obj_radius * mag_bot

    ax_norm_cam.add_patch(patches.Circle((0, 0), top_r_norm, color='#e74c3c', alpha=1.0))  # 顶部
    ax_norm_cam.add_patch(patches.Circle((0, 0), bot_r_norm, color='#c0392b', alpha=1.0))  # 底部(产生透视套匣)
    # 画出侧壁的视觉效果(透视畸变)
    ax_norm_cam.text(0, -25, f"Apparent Size: {top_r_norm:.1f}px\nSide Wall VISIBLE",
                     color='white', ha='center')

    # 远心镜头画面：顶部和底部放大率完全一样，完美重合
    top_r_tele = obj_radius * mag_tele

    ax_tele_cam.add_patch(patches.Circle((0, 0), top_r_tele, color='#e74c3c', alpha=1.0))
    ax_tele_cam.text(0, -25, f"Apparent Size: {top_r_tele:.1f}px\nSide Wall HIDDEN",
                     color='#2ecc71', ha='center', fontweight='bold')

    fig.canvas.draw_idle()


# --- 滑块 UI ---
ax_dist = plt.axes([0.2, 0.05, 0.6, 0.03], facecolor='#ecf0f1')
s_dist = Slider(ax_dist, 'Object Distance (Z)', 30, 150, valinit=70)
s_dist.on_changed(update)

update(None)
plt.show()