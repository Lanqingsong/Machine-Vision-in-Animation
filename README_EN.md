# 🤖 Machine Vision Interactive Animation Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-green.svg)](https://doc.qt.io/qtforpython/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)

**[中文版 README](README.md)**

An open-source project dedicated to teaching machine vision principles through **interactive animations**. Rather than static formulas and diagrams, every lesson lets you drag sliders and watch the physics respond in real time — making it intuitive to understand sensors, optics, noise, and calibration from the ground up.

---

## 🚀 Download & Install (Recommended for Students)

The platform is packaged as a portable `.exe` — **no Python installation required**.

### 1. Download

- **Baidu Netdisk (China)**:  
  Link: https://pan.baidu.com/s/1DpoqbZNErwVDULh5ufobxw  Code: `qgh1`

### 2. Folder Structure After Extraction

```
📁 MachinVision-Platform/
├── MachinVision-Platform.exe   ← Double-click to launch
├── python/                     ← Bundled portable Python (do NOT delete)
│   ├── python.exe
│   └── Lib/site-packages/      ← numpy, matplotlib, pillow, opencv, etc.
└── lessons/                    ← Lesson scripts (auto-created after sync)
    ├── CH-1.py
    ├── CH-2.py
    └── ...
```

> ⚠️ **Important**: Extract to a **fixed path** (e.g. `D:\CV_COURSE\`). Avoid paths with Chinese characters or spaces. Keep all folders in their relative positions.

### 3. How to Use

**First Time:**

1. Extract the archive to a fixed folder
2. Double-click `MachinVision-Platform.exe`
3. Check the Python status badge (top-left corner):
   - 🟢 **`✔ Portable Python`** — Environment ready
   - 🔴 **`✘ Python Not Found`** — Folder structure broken, re-extract
4. Click **【☁ Sync / Update Lessons】** to download the latest scripts from GitHub
5. Select a lesson from the list and click **【▶ Launch】**

**Daily Use:**

- Just double-click the `.exe`, pick a lesson, and launch
- Click **Sync** whenever new lessons are published — no need to re-download the software

---

## 📚 Course Overview

### Chapter 1 — Sensor Fundamentals

| Script | Topic | Description |
|--------|-------|-------------|
| CH-1 | Sensor Parameter Dashboard | Adjust resolution, pixel size, and frame rate; watch sensor physical dimensions and data bandwidth update in real time |
| CH-2 | Sampling & Resolution | Visualize how FOV, pixel accuracy, and minimum detectable defect size relate to each other |

### Chapter 3 — Shutter Mechanisms

| Script | Topic | Description |
|--------|-------|-------------|
| CH-3_0 | Shutter Comparison (Geometric) | Animated demo of global shutter simultaneous exposure vs. rolling shutter row-by-row scan and its skew distortion |
| CH-3_1 | Shutter Comparison (Image-based) | Full comparison with a real image and an exposure timing diagram |

### Chapter 4 — Sensor Noise

| Script | Topic | Description |
|--------|-------|-------------|
| CH-4 | Noise Model & SNR | Tune illumination, exposure, read noise, and dark current; observe non-linear SNR drop and noise source breakdown |

### Chapter 5 — Dynamic Range & HDR

| Script | Topic | Description |
|--------|-------|-------------|
| CH-5 | Dynamic Range & HDR Effect | Compare limited dynamic range imaging against HDR-processed results |
| CH-5_1 | Dynamic Range Slider | Adjust dynamic range stops and exposure offset; highlight clipped highlights and crushed shadows |
| CH-5_2 | Multi-Exposure HDR Fusion | Step through the fusion of under-, normal-, and over-exposed frames into a single HDR image |
| CH-5_3 | Tone Mapping Comparison | Interactively compare Linear, Gamma, and Reinhard HDR tone mapping algorithms with a live luminance histogram |

### Chapter 6 — Interface Selection

| Script | Topic | Description |
|--------|-------|-------------|
| CH-6 | Camera Interface Guide | Use distance and bandwidth sliders to get an interactive recommendation: USB 3.0 / GigE / Camera Link / CoaXPress |

### Chapter 7 — Lens Optics Basics

| Script | Topic | Description |
|--------|-------|-------------|
| CH-7 | Focal Length Calculator | Interactive ray diagram demonstrating f = WD × S / FOV via similar triangles |
| CH-7_1 | Lens Parameter Ray Diagram | Focal length, working distance, and sensor size update the ray diagram and FOV dynamically |
| CH-7_2 | Depth of Field & Aperture Blur | Adjust F-stop and watch foreground/background blur depth and image brightness change together |
| CH-7_3 | Circle of Confusion (CoC) | Change aperture size and off-focus object distance; compute and visualize CoC diameter in real time |

### Chapter 8 — Depth of Field Calculation

| Script | Topic | Description |
|--------|-------|-------------|
| CH-8 | DoF Dashboard | Three-parameter interactive view (focal length, aperture, focus distance) showing the light cone and asymmetric DoF zone |

### Chapter 9 — Telecentric Lenses

| Script | Topic | Description |
|--------|-------|-------------|
| CH-9 | Standard vs. Telecentric Lens | Drag the object distance slider to compare how magnification changes (or stays constant) between lens types |

### Chapter 10 — Flange Distance & Perspective Distortion

| Script | Topic | Description |
|--------|-------|-------------|
| CH-10 | C/CS-Mount Compatibility | Select lens and camera mount types plus adapter ring; check whether the combination achieves focus |
| CH-10_1 | Deep-Hole Imaging | 2×2 layout showing ray paths and camera views of a cylindrical bore under standard vs. telecentric lenses |

### Chapter 11 — Lens Distortion

| Script | Topic | Description |
|--------|-------|-------------|
| CH-11 | Spherical Aberration | Adjust the aberration coefficient; compare ideal paraxial rays with real marginal rays and the resulting magnification variation |
| CH-11_1 | Radial Distortion Demo | Tune k1/k2 on a chessboard target; observe barrel and pincushion warping and its effect on measurement accuracy |
| CH-11_2 | Distortion Correction | Apply iterative inverse-mapping correction coefficients to a pre-distorted image and watch it straighten out |

### Chapter 12 — Pixel Equivalent

| Script | Topic | Description |
|--------|-------|-------------|
| CH-12 | Pixel Equivalent Calculator | Interactive demo showing how FOV and resolution together determine physical size per pixel (mm/pixel) |

> 📌 New lessons are published by pushing scripts to the `py/` folder on GitHub. Click **Sync** in the platform to get them instantly — no software update needed.

---

## 🛠 Developer Setup (Running Source Code)

### 1. Create a Conda Environment

```bash
conda create -n mv_env python=3.10 -y
conda activate mv_env
```

### 2. Install Dependencies

```bash
pip install PySide6 requests matplotlib numpy pillow opencv-python
```

### 3. Run the Platform

```bash
python platform_launcher.py
```

### 4. Run a Single Lesson Directly

```bash
python py/CH-1.py
```

---

## 📁 Repository Structure

```
📁 Machine-Vision-in-Animation/
├── py/                        ← All lesson animation scripts
│   ├── CH-1.py                ← Sensor parameter dashboard
│   ├── CH-2.py                ← Sampling & resolution
│   └── ...                    ← 20+ interactive demos
├── platform_launcher.py       ← Desktop launcher source
├── build.spec                 ← PyInstaller packaging config
├── README.md                  ← 中文说明
└── README_EN.md               ← This file
```

> The `lessons/` directory is created locally at runtime and is not tracked by Git.

---

## 🤝 Contributing

Bug reports and feature suggestions are welcome via [Issues](https://github.com/Lanqingsong/Machine-Vision-in-Animation/issues).

**Author:** 874953727@qq.com　Bilibili: 飒飒撒旦3  
**License:** MIT

---

*If this project helps you, please give it a ⭐️ Star!*
