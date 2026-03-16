b站机器视觉源代码和文稿
这是一个为您精心设计的 `README.md`。它既包含了给普通学生看的**软件使用指南**，也包含了给想深入研究代码的同学看的**开发环境配置**。

你可以直接将以下内容复制并覆盖到你 GitHub 仓库根目录的 `README.md` 文件中。

---

# 🤖 机器视觉动画演示教学平台 (Machine-Vision-in-Animation)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-green.svg)](https://doc.qt.io/qtforpython/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)

这是一个致力于通过**交互式动画**直观展示机器视觉底层原理的开源项目。相比于枯燥的公式和静态图片，本项目通过 Python 实时模拟成像过程、噪声模型、快门机制等，帮助学生真正理解机器视觉的底层逻辑。

---

## 🚀 软件下载与安装 (推荐学生使用)

为了方便学生使用，本项目已打包成绿色版 `.exe` 软件。**无需安装 Python 环境，双击即可运行。**

### 1. 下载地址
*   **百度网盘 (国内推荐)**：
    *   链接: [https://pan.baidu.com/s/18GxhUyG4hsF7kj3iCij71A](https://pan.baidu.com/s/18GxhUyG4hsF7kj3iCij71A)
    *   提取码: **vhjs**
*   **GitHub Release**: [点击前往下载最新版本](https://github.com/Lanqingsong/Machine-Vision-in-Animation/releases)

### 2. 使用方法
1.  下载压缩包并解压到一个固定文件夹。
2.  双击运行 `机器视觉教学平台.exe`。
3.  点击界面下方的 **【☁ 同步/更新课程】** 按钮。程序会自动从 GitHub 下载最新的 `.py` 脚本及图片资源。
4.  在列表中选择课程（如 `CH-3_0`），点击 **【▶ 启动选中课程】** 即可观看演示。

---

## 📚 课程内容概览

目前已上线的部分交互式演示：
*   **CH-2 采样定理与分辨率**：直观感受 FOV、像素精度与缺陷检测的关系。
*   **CH-3 快门机制对比**：实时模拟全局快门 (Global Shutter) 与滚动快门 (Rolling Shutter) 在拍摄高速运动物体时的畸变差异。
*   **CH-4 传感器噪声模型**：调节光照、增益、读出噪声，观察信噪比 (SNR) 的非线性变化。
*   **CH-5 动态范围与 HDR**：理解图像位深与高动态范围成像的原理。
*   *更多课程内容正在持续通过 GitHub `py/` 目录更新...*

---

## 🛠 开发者环境配置 (运行源代码)

如果你希望直接运行或修改源代码（`.py`文件），请参考以下步骤配置 Python 环境：

### 1. 创建 Conda 环境
```bash
# 创建环境
conda create -n mv_env python=3.10 -y
# 激活环境
conda activate mv_env
```

### 2. 安装依赖库
```bash
pip install PySide6 requests matplotlib numpy opencv-python pillow
```

### 3. 运行程序
```bash
python CH-1.PY
```

---

## 📁 仓库结构说明
*   `/py`: 存储所有交互式动画的核心源代码。
*   `platform_launcher.py`: 桌面端主控平台源码。
*   `lessons/`: (本地运行生成) 存储同步下来的脚本及资源文件。

---

## 🤝 贡献与参与

欢迎感兴趣的老师和同学加入本项目：
*   **反馈问题**：如遇下载失败或运行报错，请在 [Issues](https://github.com/Lanqingsong/Machine-Vision-in-Animation/issues) 中提出。

**项目作者：**  874953727@qq.com b站 飒飒撒旦3
**开源协议：** MIT License

---
*如果你觉得这个项目对你有帮助，请给一个 ⭐️ Star！*
