import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QGridLayout, QFrame,
    QGraphicsDropShadowEffect, QScrollArea, QDialog
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QPixmap

# ==========================================
# 樣式定義 (採用現代深色主題 Dark Style)
# ==========================================
STYLE_SHEET = """
QMainWindow {
    background-color: #1e1e2e;
}
QLabel {
    color: #cdd6f4;
    font-family: "Segoe UI", "Microsoft JhengHei", sans-serif;
}
QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #45475a;
    border-color: #89b4fa;
}
QPushButton:pressed {
    background-color: #89b4fa;
    color: #11111b;
}
QFrame#Card {
    background-color: #181825;
    border-radius: 10px;
    border: 1px solid #313244;
}
"""

# ==========================================
# 頁面 1: 資訊管理 (平面圖1 - 電腦與機櫃)
# ==========================================
class ITManagementPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        header = QLabel("🖥️ 資訊管理 - 室內設備配置與 ESP32 在線狀態圖")
        header.setFont(QFont("Microsoft JhengHei", 14, QFont.Weight.Bold))
        layout.addWidget(header)

        # 模擬平面圖網格
        grid = QGridLayout()
        grid.setSpacing(15)

        # 機櫃 42U 示意圖
        rack_card = QFrame()
        rack_card.setObjectName("Card")
        rack_layout = QVBoxLayout(rack_card)
        rack_title = QLabel("📦 42U 主機櫃\n(File Server / Mail / FTP / UPS)")
        rack_title.setStyleSheet("color: #f9e2af; font-weight: bold;")
        rack_layout.addWidget(rack_title)
        grid.addWidget(rack_card, 0, 0, 1, 2)

        # 模擬 20 台 PC 的 ESP32 狀態
        self.pc_status_labels = []
        for i in range(20):
            pc_card = QFrame()
            pc_card.setObjectName("Card")
            pc_lay = QVBoxLayout(pc_card)
            
            pc_name = QLabel(f"PC-{i+1:02d}")
            pc_name.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            
            # ESP32 狀態標籤 (以動態顏色區分)
            status_lbl = QLabel("ESP32: ON" if i % 3 != 0 else "ESP32: OFF")
            status_color = "#a6e3a1" if i % 3 != 0 else "#f38ba8"
            status_lbl.setStyleSheet(f"color: {status_color}; font-weight: bold;")
            
            pc_lay.addWidget(pc_name)
            pc_lay.addWidget(status_lbl)
            
            row = (i // 5) + 1
            col = i % 5
            grid.addWidget(pc_card, row, col)

        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(grid)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        layout.addWidget(scroll)

# ==========================================
# 頁面 2: 電能管理 (配電盤迴路即時監控)
# ==========================================
class PowerManagementPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        header = QLabel("⚡ 電能管理 - 全戶配電盤即時負載 (100A 總容量)")
        header.setFont(QFont("Microsoft JhengHei", 14, QFont.Weight.Bold))
        layout.addWidget(header)

        grid = QGridLayout()
        grid.setSpacing(15)

        # 220V 30A (4 迴路)
        for i in range(4):
            card = QFrame()
            card.setObjectName("Card")
            lay = QVBoxLayout(card)
            lay.addWidget(QLabel(f"⚡ 迴路 A{i+1} (220V / 30A)"))
            
            # 模擬即時數值
            val_lbl = QLabel(f"電壓: 220.2 V\n電流: {5.2 + i*1.1:.1f} A\n功耗: {(220.2 * (5.2 + i*1.1))/1000:.2f} kW")
            val_lbl.setStyleSheet("color: #89b4fa;")
            lay.addWidget(val_lbl)
            grid.addWidget(card, 0, i)

        # 110V 20A (6 迴路)
        for i in range(6):
            card = QFrame()
            card.setObjectName("Card")
            lay = QVBoxLayout(card)
            lay.addWidget(QLabel(f"💡 迴路 B{i+1} (110V / 20A)"))
            
            val_lbl = QLabel(f"電壓: 110.5 V\n電流: {2.1 + i*0.8:.1f} A\n功耗: {(110.5 * (2.1 + i*0.8))/1000:.2f} kW")
            val_lbl.setStyleSheet("color: #a6e3a1;")
            lay.addWidget(val_lbl)
            row = 1 + (i // 3)
            col = (i % 3) * 1  # 跨格美化
            grid.addWidget(card, row, col, 1, 1)

        layout.addLayout(grid)

# ==========================================
# 頁面 3: 安防管理 (平面圖2 - 門禁/攝影機/磁簧)
# ==========================================
class SecurityManagementPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        header = QLabel("🛡️ 安防管理 - 平面監控與即時訊號 (點擊圖示進入單一畫面)")
        header.setFont(QFont("Microsoft JhengHei", 14, QFont.Weight.Bold))
        layout.addWidget(header)

        grid = QGridLayout()
        
        # 大門門禁鎖
        door_btn = QPushButton("🚪 大門刷卡機 & 磁力鎖\n[狀態: 鎖定中]")
        door_btn.setStyleSheet("background-color: #313244; color: #a6e3a1; min-height: 80px;")
        door_btn.clicked.connect(lambda: self.open_camera_dialog("大門門禁刷卡機 CCTV-01"))
        grid.addWidget(door_btn, 0, 0, 1, 2)

        # 6 隻攝影機
        for i in range(6):
            cam_btn = QPushButton(f"📷 網路鏡頭 #{i+1}")
            cam_btn.setStyleSheet("min-height: 60px;")
            cam_btn.clicked.connect(lambda ch, idx=i+1: self.open_camera_dialog(f"網路監控鏡頭 CAM-{idx:02d}"))
            grid.addWidget(cam_btn, 1 + (i // 3), (i % 3) * 2)

        # 5 道窗戶磁簧開關
        for i in range(5):
            win_btn = QPushButton(f"🪟 窗戶磁簧 #{i+1}\n[正常閉合]")
            win_btn.setStyleSheet("min-height: 50px; color: #b4befe;")
            win_btn.clicked.connect(lambda ch, idx=i+1: self.open_camera_dialog(f"窗戶磁簧 #{idx} 連動畫面"))
            grid.addWidget(win_btn, 3, i)

        layout.addLayout(grid)

    def open_camera_dialog(self, title):
        dlg = QDialog(self)
        dlg.setWindowTitle(f"即時監控畫面 - {title}")
        dlg.resize(400, 300)
        lay = QVBoxLayout(dlg)
        img_lbl = QLabel(f"🎥 {title}\nRTSP 即時串流播放區域 (1080p)")
        img_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_lbl.setStyleSheet("background-color: #000; color: #00ff00; font-size: 16px;")
        lay.addWidget(img_lbl)
        dlg.exec()

# ==========================================
# 主視窗 (整合三大功能)
# ==========================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("中小企業智慧營運整合管理系統 UI")
        self.resize(1100, 700)
        self.setStyleSheet(STYLE_SHEET)

        # 中央主 UI 佈局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 1. 頂部選單按鈕列 (三大主功能)
        nav_layout = QHBoxLayout()
        
        self.btn_it = QPushButton("💻 資訊管理 (IT)")
        self.btn_power = QPushButton("⚡ 電能管理 (Power)")
        self.btn_sec = QPushButton("🛡️ 安防管理 (Security)")

        for btn in (self.btn_it, self.btn_power, self.btn_sec):
            btn.setFixedHeight(50)
            btn.setFont(QFont("Microsoft JhengHei", 12, QFont.Weight.Bold))
            nav_layout.addWidget(btn)

        main_layout.addLayout(nav_layout)

        # 2. 中間多頁切換區域 (QStackedWidget)
        self.stacked_widget = QStackedWidget()
        
        self.page_it = ITManagementPage()
        self.page_power = PowerManagementPage()
        self.page_sec = SecurityManagementPage()

        self.stacked_widget.addWidget(self.page_it)
        self.stacked_widget.addWidget(self.page_power)
        self.stacked_widget.addWidget(self.page_sec)

        main_layout.addWidget(self.stacked_widget)

        # 事件綁定
        self.btn_it.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_power.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_sec.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        # 預設顯示第一頁
        self.stacked_widget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())