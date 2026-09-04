import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                             QLabel, QVBoxLayout, QHBoxLayout, QStackedWidget, 
                             QGridLayout, QFrame, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor

class SmartOfficeUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("中小企業智慧管理系統 (Enterprise 3-in-1 Management UI)")
        self.setGeometry(100, 100, 1024, 768)
        self.setStyleSheet("background-color: #2F3542; color: #FFFFFF;")
        
        # 初始化中央主視窗與堆疊布局（用於切換頁面）
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        self.stacked_widget = QStackedWidget()
        
        # 建立各個頁面
        self.create_home_page()
        self.create_info_page()
        self.create_power_page()
        self.create_security_page()
        
        self.main_layout.addWidget(self.stacked_widget)
        
        # 啟動模擬數據定時器（模擬 ESP32 數據變更）
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_live_data)
        self.timer.start(2000) # 每2秒更新一次

    # ==========================================
    # 📌 頁面 0: 主頁面 (Home Page)
    # ==========================================
    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("中小企業智慧管理系統")
        title.setFont(QFont("Microsoft JhengHei", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("margin-top: 50px; margin-bottom: 50px; color: #1E90FF;")
        layout.addWidget(title)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(30)
        
        modules = [
            ("資訊管理\n(IT Management)", "#2ED573", 1),
            ("電能管理\n(Power Management)", "#FFA502", 2),
            ("安防管理\n(Security Management)", "#FF4757", 3)
        ]
        
        for name, color, page_idx in modules:
            btn = QPushButton(name)
            btn.setFont(QFont("Microsoft JhengHei", 18, QFont.Weight.Bold))
            btn.setFixedSize(260, 200)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border-radius: 15px;
                }}
                QPushButton:hover {{
                    background-color: white;
                    color: {color};
                    border: 3px solid {color};
                }}
            """)
            btn.clicked.connect(lambda checked, idx=page_idx: self.stacked_widget.setCurrentIndex(idx))
            btn_layout.addWidget(btn)
            
        layout.addLayout(btn_layout)
        layout.addStretch()
        self.stacked_widget.addWidget(page)

    # ==========================================
    # 📌 頁面 1: 資訊管理 (IT Page)
    # ==========================================
    def create_info_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(self.get_back_button())
        
        title = QLabel("資訊管理 - 室內平面圖 1 (工作站與機櫃狀態)")
        title.setFont(QFont("Microsoft JhengHei", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        content_layout = QHBoxLayout()
        
        # 左側：20台PC平面模擬配置
        pc_frame = QFrame()
        pc_frame.setFrameShape(QFrame.Shape.StyledPanel)
        pc_frame.setStyleSheet("border: 2px solid #57606F; border-radius: 10px; background-color: #341F97;")
        pc_grid = QGridLayout(pc_frame)
        
        self.pc_buttons = {}
        # 模擬 20 台辦公桌 PC 配置 (4x5 矩陣)
        pc_count = 1
        for row in range(4):
            for col in range(5):
                pc_id = f"PC-{pc_count:02d}"
                btn = QPushButton(f"💻\n{pc_id}\n偵測中")
                btn.setFont(QFont("Microsoft JhengHei", 10))
                btn.setFixedSize(90, 80)
                pc_grid.addWidget(btn, row, col)
                self.pc_buttons[pc_id] = btn
                pc_count += 1
                
        content_layout.addWidget(pc_frame, 3)
        
        # 右側：42U 機櫃 (包含各 Server 與 UPS)
        rack_frame = QFrame()
        rack_frame.setFrameShape(QFrame.Shape.StyledPanel)
        rack_frame.setStyleSheet("border: 2px solid #1E90FF; border-radius: 10px; background-color: #1E272E;")
        rack_layout = QVBoxLayout(rack_frame)
        
        rack_title = QLabel("🔒 42U 機櫃總覽")
        rack_title.setFont(QFont("Microsoft JhengHei", 14, QFont.Weight.Bold))
        rack_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rack_layout.addWidget(rack_title)
        
        servers = [("File Server", "🟢 正常"), ("Mail Server", "🟢 正常"), ("FTP Server", "🟢 正常"), ("UPS 不斷電系統", "🔋 100%")]
        for s_name, status in servers:
            lbl = QLabel(f"【{s_name}】\n狀態: {status}")
            lbl.setFont(QFont("Microsoft JhengHei", 11))
            lbl.setStyleSheet("background-color: #2F3542; padding: 10px; border-radius: 5px; margin: 5px;")
            rack_layout.addWidget(lbl)
            
        content_layout.addWidget(rack_frame, 1)
        layout.addLayout(content_layout)
        self.stacked_widget.addWidget(page)

    # ==========================================
    # 📌 頁面 2: 電能管理 (Power Page)
    # ==========================================
    def create_power_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(self.get_back_button())
        
        title = QLabel("電能管理 - 全戶配電盤模擬圖 (ESP32 即時數據換算)")
        title.setFont(QFont("Microsoft JhengHei", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # 配電盤外框
        panel_frame = QFrame()
        panel_frame.setStyleSheet("border: 3px solid #FFA502; border-radius: 10px; background-color: #1E272E; padding: 15px;")
        panel_layout = QVBoxLayout(panel_frame)
        
        # 100A 總開關
        self.main_breaker = QLabel("⚡ 總配電盤主開關 (Total Capacity: 100A) | 總功率計算中...")
        self.main_breaker.setFont(QFont("Microsoft JhengHei", 14, QFont.Weight.Bold))
        self.main_breaker.setStyleSheet("background-color: #FF4757; color: white; padding: 12px; border-radius: 5px;")
        self.main_breaker.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(self.main_breaker)
        
        breakers_layout = QHBoxLayout()
        
        # 左側：220V 30A 4迴路 (通常供冷氣/重電)
        v220_layout = QVBoxLayout()
        v220_title = QLabel("🔴 220V 30A 高耗電迴路 (x4)")
        v220_title.setFont(QFont("Microsoft JhengHei", 12, QFont.Weight.Bold))
        v220_layout.addWidget(v220_title)
        
        self.v220_labels = []
        for i in range(4):
            lbl = QLabel(f"迴路 A{i+1} (220V)\n電流: 0.0 A\n功率: 0 W")
            lbl.setStyleSheet("background-color: #2F3542; border: 1px solid #747D8C; padding: 10px; border-radius: 5px;")
            v220_layout.addWidget(lbl)
            self.v220_labels.append(lbl)
        breakers_layout.addLayout(v220_layout)
        
        # 右側：110V 20A 6迴路 (供照明/一般插座)
        v110_layout = QVBoxLayout()
        v110_title = QLabel("🔵 110V 20A 一般辦公迴路 (x6)")
        v110_title.setFont(QFont("Microsoft JhengHei", 12, QFont.Weight.Bold))
        v110_layout.addWidget(v110_title)
        
        self.v110_labels = []
        for i in range(6):
            lbl = QLabel(f"迴路 B{i+1} (110V)\n電流: 0.0 A\n功率: 0 W")
            lbl.setStyleSheet("background-color: #2F3542; border: 1px solid #747D8C; padding: 6px; border-radius: 5px;")
            v110_layout.addWidget(lbl)
            self.v110_labels.append(lbl)
        breakers_layout.addLayout(v110_layout)
        
        panel_layout.addLayout(breakers_layout)
        layout.addWidget(panel_frame)
        self.stacked_widget.addWidget(page)

    # ==========================================
    # 📌 頁面 3: 安防管理 (Security Page)
    # ==========================================
    def create_security_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(self.get_back_button())
        
        title = QLabel("安防管理 - 室內平面圖 2 (周界安全與監控門禁點擊)")
        title.setFont(QFont("Microsoft JhengHei", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # 模擬平面圖佈局容器
        map_frame = QFrame()
        map_frame.setStyleSheet("border: 2px solid #FF4757; border-radius: 10px; background-color: #222f3e; position: relative;")
        map_grid = QGridLayout(map_frame)
        
        # 1. 網路型門禁刷卡機 (大門磁力鎖)
        gate_btn = QPushButton("🚪 大門管制點\n[網路門禁刷卡機]\n磁力鎖: 鎖定中")
        gate_btn.setStyleSheet("background-color: #10AC84; color: white; font-weight: bold; border-radius: 8px;")
        gate_btn.setFixedSize(160, 80)
        gate_btn.clicked.connect(lambda: self.trigger_camera_view("大門入口門禁解鎖記錄與即時串流"))
        map_grid.addWidget(gate_btn, 0, 2) # 置於上方大門位置
        
        # 2. 6 隻網路型監控鏡頭 (CCTV 1 ~ 6)
        self.cams = []
        for i in range(6):
            cam_btn = QPushButton(f"📹 鏡頭 CAM-{i+1}\n[點擊看畫面]")
            cam_btn.setStyleSheet("background-color: #2E86DE; color: white; border-radius: 5px;")
            cam_btn.setFixedSize(120, 60)
            cam_btn.clicked.connect(lambda checked, idx=i+1: self.trigger_camera_view(f"網路型監控鏡頭 CAM-{idx} 即時畫面"))
            self.cams.append(cam_btn)
            
        # 將鏡頭分佈在平面圖四角與通道
        map_grid.addWidget(self.cams[0], 0, 0)
        map_grid.addWidget(self.cams[1], 0, 4)
        map_grid.addWidget(self.cams[2], 2, 0)
        map_grid.addWidget(self.cams[3], 2, 4)
        map_grid.addWidget(self.cams[4], 4, 1)
        map_grid.addWidget(self.cams[5], 4, 3)
        
        # 3. 5 道窗戶磁簧開關
        for i in range(5):
            reed_btn = QPushButton(f"🧲 窗戶磁簧-{i+1}\n[🟢 閉合]")
            reed_btn.setStyleSheet("background-color: #8395A7; color: white; font-size: 11px;")
