import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from PIL import Image
import os


# 1. 加载并预处理图像
def load_base_image(path):
    if os.path.exists(path):
        img = Image.open(path).convert('L')  # 转为灰度图便于展示噪声
        img = img.resize((300, 300))  # 缩放以提高处理速度
        return np.array(img) / 255.0  # 归一化到 [0, 1]
    else:
        # 如果文件不存在，创建一个模拟边缘的图案
        grid = np.zeros((300, 300))
        grid[50:-50, 50:-50] = 0.5
        grid[100:-100, 100:-100] = 1.0
        return grid


base_img = load_base_image('1.png')

# 2. 设置布局
fig = plt.figure(figsize=(15, 8), facecolor='#f4f7f6')
plt.subplots_adjust(left=0.1, bottom=0.3, right=0.95, top=0.9, wspace=0.3)

ax_img = fig.add_subplot(131)  # 视觉显示
ax_snr = fig.add_subplot(132)  # SNR 曲线
ax_noise = fig.add_subplot(133)  # 噪声分量统计


def update(val):
    # 获取滑动条参数
    s_val = s_light.val  # 光照强度 (单位: 峰值光子数)
    t_exp = s_time.val  # 曝光时间
    read_n = s_read.val  # 读出噪声标准差
    dark_c = s_dark.val  # 暗电流强度

    # --- 物理模拟过程 ---
    # 1. 信号形成 (受光照和曝光时间影响)
    # 假设 base_img 的 1.0 代表满阱容量的一部分
    pure_signal = base_img * s_val * t_exp

    # 2. 引入光子散粒噪声 (泊松分布: 均值为信号强度)
    # 用正态分布模拟大数下的泊松分布: std = sqrt(signal)
    shot_noise_map = np.random.normal(0, np.sqrt(np.maximum(pure_signal, 0)))

    # 3. 引入暗电流噪声 (随时间增加)
    dark_noise_std = np.sqrt(dark_c * t_exp)
    dark_noise_map = np.random.normal(0, dark_noise_std, base_img.shape)

    # 4. 引入读出噪声 (固定电路噪声)
    read_noise_map = np.random.normal(0, read_n, base_img.shape)

    # 最终图像 = 信号 + 所有噪声叠加
    noisy_img = pure_signal + shot_noise_map + dark_noise_map + read_noise_map

    # --- 计算 SNR ---
    avg_signal = np.mean(pure_signal)
    total_noise_std = np.sqrt(avg_signal + (dark_c * t_exp) + read_n ** 2)
    snr_linear = avg_signal / total_noise_std if total_noise_std > 0 else 0
    snr_db = 20 * np.log10(snr_linear) if snr_linear > 0 else -20

    # --- 界面更新 ---
    # 1. 图像展示: 自动调整显示范围以观察细节
    ax_img.clear()
    ax_img.imshow(noisy_img, cmap='gray')
    ax_img.set_title(f"VISUAL: {snr_db:.1f} dB\n(Real Image Details)", fontsize=12, fontweight='bold')
    ax_img.axis('off')

    # 2. SNR 曲线更新
    ax_snr.clear()
    ax_snr.set_title("LOGIC: SNR Non-linear Drop", fontsize=11, fontweight='bold')
    x_range = np.linspace(1, 1000, 50)
    # 曲线公式: SNR = S / sqrt(S + Dark + Read^2)
    y_range = [20 * np.log10((x * t_exp) / np.sqrt(x * t_exp + dark_c * t_exp + read_n ** 2)) for x in x_range]
    ax_snr.plot(x_range, y_range, color='#2ecc71', lw=2, label='SNR Curve')
    ax_snr.scatter([s_val], [snr_db], color='red', s=100, zorder=5)  # 当前点
    ax_snr.set_xlabel("Light Level (Photons/px)")
    ax_snr.set_ylabel("SNR (dB)")
    ax_snr.grid(True, alpha=0.3)

    # 3. 噪声分解更新 (方差贡献)
    ax_noise.clear()
    ax_noise.set_title("SOURCE: Noise Variance Contribution", fontsize=11, fontweight='bold')
    noise_names = ['Read', 'Dark', 'Shot']
    variances = [read_n ** 2, dark_c * t_exp, avg_signal]
    bars = ax_noise.bar(noise_names, variances, color=['#e74c3c', '#9b59b6', '#3498db'])
    ax_noise.set_yscale('log')  # 对数坐标更易观察
    ax_noise.set_ylabel("Variance ($\sigma^2$)")

    fig.canvas.draw_idle()


# --- 滑动条设置 ---
ax_color = '#dfe6e9'
s_light = Slider(plt.axes([0.2, 0.18, 0.6, 0.03], facecolor=ax_color), 'Light Level', 1, 1000, valinit=500)
s_time = Slider(plt.axes([0.2, 0.14, 0.6, 0.03], facecolor=ax_color), 'Exposure', 0.1, 5.0, valinit=1.0)
s_read = Slider(plt.axes([0.2, 0.10, 0.6, 0.03], facecolor=ax_color), 'Read Noise', 0.1, 50, valinit=15)
s_dark = Slider(plt.axes([0.2, 0.06, 0.6, 0.03], facecolor=ax_color), 'Dark Current', 0, 100, valinit=10)

s_light.on_changed(update)
s_time.on_changed(update)
s_read.on_changed(update)
s_dark.on_changed(update)

update(None)
plt.show()