import sys
import os
import subprocess
import requests
import re
import shutil
import webbrowser
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QListWidget, QPushButton, QLabel,
                               QMessageBox, QStatusBar, QFrame)
from PySide6.QtCore import Qt, QThread, Signal, QSize
from PySide6.QtGui import QFont, QColor, QPalette

# --- 配置区 ---
USER = "Lanqingsong"
REPO = "Machine-Vision-in-Animation"
FOLDER = "py"
BRANCH = "main"

WEB_URL = f"https://github.com/{USER}/{REPO}/tree/{BRANCH}/{FOLDER}"
GITHUB_API_URL = f"https://api.github.com/repos/{USER}/{REPO}/contents/{FOLDER}"
PROXY_URL = "https://ghproxy.net/https://raw.githubusercontent.com"

# ------------------------------------------------------------------ #
#  关键修复1：路径基准
#  - 打包后 sys.frozen = True，exe 所在目录作为基准
#  - 开发时用脚本自身所在目录
# ------------------------------------------------------------------ #
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOCAL_DIR = os.path.join(BASE_DIR, "lessons")


# ------------------------------------------------------------------ #
#  关键修复2：找到能运行 .py 文件的 Python 解释器
#  优先级：便携版 > 系统环境变量
# ------------------------------------------------------------------ #
def get_python_executable():
    """
    打包后 sys.executable 是 launcher.exe 本身，不能用于运行子脚本。
    依次寻找：
      1. exe 旁边的 python/python.exe（便携版，推荐）
      2. 系统 PATH 里的 python / python3
    """
    # 1. 便携版 Python（Windows）
    portable_win = os.path.join(BASE_DIR, "python", "python.exe")
    if os.path.exists(portable_win):
        return portable_win

    # 2. 便携版 Python（macOS / Linux，以防跨平台）
    portable_unix = os.path.join(BASE_DIR, "python", "bin", "python3")
    if os.path.exists(portable_unix):
        return portable_unix

    # 3. 系统环境变量
    system_python = shutil.which("python") or shutil.which("python3")
    if system_python:
        return system_python

    return None  # 找不到任何 Python


def natural_sort_key(s):
    return [int(t) if t.isdigit() else t.lower()
            for t in re.split(r'(\d+)', s)]


# ------------------------------------------------------------------ #
#  后台同步线程
# ------------------------------------------------------------------ #
class UpdateWorker(QThread):
    finished = Signal(bool, str)
    progress = Signal(str)

    def run(self):
        try:
            os.makedirs(LOCAL_DIR, exist_ok=True)
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(GITHUB_API_URL, headers=headers, timeout=12)

            if response.status_code == 200:
                files = response.json()
                py_count = 0
                for file_info in files:
                    name = file_info['name']
                    if name.endswith(('.py', '.png', '.jpg', '.jpeg')):
                        self.progress.emit(f"正在同步: {name}")
                        raw_url = f"{PROXY_URL}/{USER}/{REPO}/{BRANCH}/{FOLDER}/{name}"
                        file_data = requests.get(raw_url, timeout=15).content
                        with open(os.path.join(LOCAL_DIR, name), "wb") as f:
                            f.write(file_data)
                        if name.endswith('.py'):
                            py_count += 1
                self.finished.emit(True, f"同步成功！共更新 {py_count} 个课程脚本。")
            else:
                self.finished.emit(False, f"GitHub API 访问受限 (错误码: {response.status_code})")
        except Exception as e:
            self.finished.emit(False, str(e))


# ------------------------------------------------------------------ #
#  主窗口
# ------------------------------------------------------------------ #
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("机器视觉动画教学平台")
        self.setMinimumSize(720, 540)
        self._apply_theme()
        self._init_ui()
        self._check_python()
        self.refresh_list()

    # -------------------------------------------------------------- #
    #  主题样式
    # -------------------------------------------------------------- #
    def _apply_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background: #0d1117;
            }
            QWidget#central {
                background: #0d1117;
            }
            QLabel#title {
                color: #e6edf3;
                font-size: 22px;
                font-weight: bold;
                letter-spacing: 2px;
                padding: 8px 4px 0px 4px;
            }
            QLabel#subtitle {
                color: #8b949e;
                font-size: 12px;
                padding: 0px 4px 8px 4px;
            }
            QLabel#python_status {
                font-size: 11px;
                padding: 2px 6px;
                border-radius: 4px;
            }
            QFrame#divider {
                background: #21262d;
                max-height: 1px;
            }
            QListWidget {
                background: #161b22;
                border: 1px solid #21262d;
                border-radius: 8px;
                font-size: 14px;
                color: #c9d1d9;
                outline: none;
                padding: 4px;
            }
            QListWidget::item {
                padding: 12px 16px;
                border-radius: 6px;
                margin: 2px 0px;
            }
            QListWidget::item:hover {
                background: #1f2937;
                color: #e6edf3;
            }
            QListWidget::item:selected {
                background: #1a3a5c;
                color: #58a6ff;
                border-left: 3px solid #58a6ff;
            }
            QPushButton#btn_run {
                background: #238636;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                height: 48px;
                padding: 0 20px;
            }
            QPushButton#btn_run:hover {
                background: #2ea043;
            }
            QPushButton#btn_run:pressed {
                background: #1a6325;
            }
            QPushButton#btn_run:disabled {
                background: #21262d;
                color: #484f58;
            }
            QPushButton#btn_update {
                background: #1f2937;
                color: #58a6ff;
                border: 1px solid #30363d;
                border-radius: 6px;
                font-size: 13px;
                height: 48px;
                padding: 0 16px;
            }
            QPushButton#btn_update:hover {
                background: #1a3a5c;
                border-color: #58a6ff;
            }
            QPushButton#btn_update:disabled {
                color: #484f58;
                border-color: #21262d;
            }
            QPushButton#btn_refresh {
                background: transparent;
                color: #8b949e;
                border: 1px solid #30363d;
                border-radius: 6px;
                font-size: 13px;
                height: 48px;
                padding: 0 14px;
            }
            QPushButton#btn_refresh:hover {
                color: #c9d1d9;
                border-color: #8b949e;
            }
            QStatusBar {
                background: #161b22;
                color: #8b949e;
                font-size: 11px;
                border-top: 1px solid #21262d;
            }
        """)

    # -------------------------------------------------------------- #
    #  UI 布局
    # -------------------------------------------------------------- #
    def _init_ui(self):
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 16, 20, 8)
        layout.setSpacing(10)

        # 标题栏
        header = QHBoxLayout()
        title_block = QVBoxLayout()
        title_block.setSpacing(2)

        title = QLabel("机器视觉 · 动画教学平台")
        title.setObjectName("title")
        subtitle = QLabel("Machine Vision Interactive Animation Launcher")
        subtitle.setObjectName("subtitle")
        title_block.addWidget(title)
        title_block.addWidget(subtitle)
        header.addLayout(title_block)
        header.addStretch()

        self.lbl_python = QLabel()
        self.lbl_python.setObjectName("python_status")
        header.addWidget(self.lbl_python)

        layout.addLayout(header)

        # 分割线
        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFrameShape(QFrame.HLine)
        layout.addWidget(divider)

        # 课程列表
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # 按钮区
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_run = QPushButton("▶  启动选中课程")
        self.btn_run.setObjectName("btn_run")
        self.btn_run.clicked.connect(self.run_lesson)

        self.btn_update = QPushButton("☁  同步 / 更新课程")
        self.btn_update.setObjectName("btn_update")
        self.btn_update.clicked.connect(self.update_from_git)

        self.btn_refresh = QPushButton("↻  刷新列表")
        self.btn_refresh.setObjectName("btn_refresh")
        self.btn_refresh.clicked.connect(self.refresh_list)

        btn_layout.addWidget(self.btn_run, 3)
        btn_layout.addWidget(self.btn_update, 2)
        btn_layout.addWidget(self.btn_refresh, 1)
        layout.addLayout(btn_layout)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"就绪  |  课程目录: {LOCAL_DIR}")

    # -------------------------------------------------------------- #
    #  Python 解释器检测
    # -------------------------------------------------------------- #
    def _check_python(self):
        python_exe = get_python_executable()
        if python_exe:
            name = os.path.basename(os.path.dirname(python_exe)) \
                if "python" in os.path.dirname(python_exe).lower() else "系统"
            # 便携版判断
            if os.path.join(BASE_DIR, "python") in python_exe:
                label = "✔  便携 Python"
                style = "background:#1a3a2a; color:#3fb950;"
            else:
                label = f"✔  系统 Python"
                style = "background:#1a3a5c; color:#58a6ff;"
        else:
            label = "✘  未找到 Python"
            style = "background:#3a1a1a; color:#f85149;"

        self.lbl_python.setText(label)
        self.lbl_python.setStyleSheet(
            f"font-size:11px; padding:3px 10px; border-radius:4px; {style}"
        )
        self.btn_run.setEnabled(python_exe is not None)

    # -------------------------------------------------------------- #
    #  刷新课程列表
    # -------------------------------------------------------------- #
    def refresh_list(self):
        self.list_widget.clear()
        if not os.path.exists(LOCAL_DIR):
            self.status_bar.showMessage(f"⚠ 课程目录不存在: {LOCAL_DIR}  请先点击「同步」")
            return

        files = [f for f in os.listdir(LOCAL_DIR)
                 if f.startswith('CH-') and f.endswith('.py')]
        sorted_files = sorted(files, key=natural_sort_key)
        self.list_widget.addItems(sorted_files)

        count = len(sorted_files)
        self.status_bar.showMessage(
            f"共找到 {count} 个课程  |  目录: {LOCAL_DIR}"
        )

    # -------------------------------------------------------------- #
    #  启动课程
    # -------------------------------------------------------------- #
    def run_lesson(self):
        selected = self.list_widget.currentItem()
        if not selected:
            QMessageBox.warning(self, "提示", "请先从列表中选择一个课程！")
            return

        python_exe = get_python_executable()
        if not python_exe:
            QMessageBox.critical(
                self, "找不到 Python 解释器",
                "程序无法找到可用的 Python 解释器。\n\n"
                "请在程序旁边放置 python/ 目录（便携版），\n"
                "或确保系统已安装 Python 并加入 PATH。"
            )
            return

        file_name = selected.text()
        self.status_bar.showMessage(f"▶  正在启动: {file_name}")

        try:
            # 工作目录设为 lessons/，确保脚本内相对路径（如读取图片）正常
            subprocess.Popen(
                [python_exe, file_name],
                cwd=LOCAL_DIR,
                # 在 Windows 上隐藏控制台窗口（可选，打开后调试时可注释掉）
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
        except Exception as e:
            QMessageBox.critical(self, "启动失败", f"无法运行脚本:\n{str(e)}")

    # -------------------------------------------------------------- #
    #  同步/更新
    # -------------------------------------------------------------- #
    def update_from_git(self):
        self.btn_update.setEnabled(False)
        self.btn_refresh.setEnabled(False)
        self.status_bar.showMessage("正在连接 GitHub 仓库...")
        self.worker = UpdateWorker()
        self.worker.progress.connect(lambda m: self.status_bar.showMessage(m))
        self.worker.finished.connect(self._on_update_finished)
        self.worker.start()

    def _on_update_finished(self, success, msg):
        self.btn_update.setEnabled(True)
        self.btn_refresh.setEnabled(True)
        self.refresh_list()

        if success:
            QMessageBox.information(self, "同步成功", msg)
            self.status_bar.showMessage("✔  资源已同步至最新")
        else:
            reply = QMessageBox.critical(
                self,
                "同步失败",
                f"由于网络原因或访问频率限制，同步未能完成。\n\n"
                f"错误详情：{msg}\n\n"
                f"建议操作：\n"
                f"  1. 检查网络 / 科学上网环境后重试\n"
                f"  2. 点击「访问网页」手动下载文件到 lessons/ 文件夹\n\n"
                f"项目地址：{WEB_URL}",
                QMessageBox.StandardButton.Retry |
                QMessageBox.StandardButton.Close |
                QMessageBox.StandardButton.Open,
                QMessageBox.StandardButton.Retry
            )
            if reply == QMessageBox.StandardButton.Retry:
                self.update_from_git()
            elif reply == QMessageBox.StandardButton.Open:
                webbrowser.open(WEB_URL)


# ------------------------------------------------------------------ #
#  入口
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # 全局深色 Palette（防止部分控件继承系统浅色）
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#0d1117"))
    palette.setColor(QPalette.WindowText, QColor("#e6edf3"))
    palette.setColor(QPalette.Base, QColor("#161b22"))
    palette.setColor(QPalette.AlternateBase, QColor("#21262d"))
    palette.setColor(QPalette.Text, QColor("#c9d1d9"))
    palette.setColor(QPalette.Button, QColor("#21262d"))
    palette.setColor(QPalette.ButtonText, QColor("#c9d1d9"))
    palette.setColor(QPalette.Highlight, QColor("#1a3a5c"))
    palette.setColor(QPalette.HighlightedText, QColor("#58a6ff"))
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())