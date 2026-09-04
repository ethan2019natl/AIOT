import sys
import socket
import struct
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, 
                             QPushButton, QMessageBox, QHeaderView, QGroupBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor

# ==============================================================================
# 1. 背景執行緒：負責處理網路控制指令（避免按按鈕時網管主控台卡死）
# ==============================================================================
class RemoteControlWorker(QThread):
    status_signal = pyqtSignal(str) # 回傳執行狀態文字

    def __init__(self, action, ip, mac=None):
        super().__init__()
        self.action = action
        self.ip = ip
        self.mac = mac

    def send_wol(self):
        """ 發送 Wake-on-LAN 魔術封包喚醒電腦 """
        if not self.mac:
            return False
        try:
            # 格式化 MAC 地址
            clean_mac = self.mac.replace("-", "").replace(":", "")
            data = bytes.fromhex('FFFFFFFFFFFF' + clean_mac * 16)
            # 透過 UDP 廣播發送 (預設使用 9 號連接埠)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(data, ('255.255.255.255', 9))
            sock.close()
            return True
        except Exception as e:
            print(f"WOL 失敗: {e}")
            return False

    def send_agent_cmd(self, command):
        """ 傳送指令給部署在員工電腦上的 Python Agent (監聽 50001 埠) """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3.0) # 3秒連線逾時
                s.connect((self.ip, 50001))
                s.sendall(command.encode('utf-8'))
                response = s.recv(1024).decode('utf-8')
                return True, response
        except Exception as e:
            return False, f"連線失敗 ({str(e)})"

    def run(self):
        if self.action == "WOL":
            success = self.send_wol()
            self.status_signal.emit("已發送喚醒封包" if success else "喚醒發送失敗")
        
        elif self.action == "SHUTDOWN":
            success, msg = self.send_agent_cmd("CMD_SHUTDOWN")
            self.status_signal.emit("已關機" if success else msg)
            
        elif self.action == "REBOOT":
            success, msg = self.send_agent_cmd("CMD_REBOOT")
            self.status_signal.emit("已重啟" if success else msg)
            
        elif self.action == "ENTER_LINUX_BACKUP":
            success, msg = self.send_agent_cmd("CMD_BOOT_LINUX_BACKUP")
            self.status_signal.emit("引導成功，重啟中" if success else msg)

# ==============================================================================
# 2. 前端主控台畫面 UI
# ==============================================================================
class AdminConsoleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_pc_list()

    def initUI(self):
        self.setWindowTitle("企業網管主控台 - 10台辦公室電腦連線管理工具")
        self.resize(1150, 600)
        
        # 網管風黑綠配色樣式表
        self.setStyleSheet("""
            QMainWindow { background-color: #1a1c20; }
            QLabel { color: #ecf0f1; font-size: 14px; }
            QTableWidget { 
                background-color: #242830; color: #ffffff; 
                gridline-color: #3a3f4d; border: 1px solid #3a3f4d;
                font-size: 13px;
            }
            QTableWidget::item { padding: 5px; }
            QHeaderView::section { 
                background-color: #2f3440; color: #00ff66; 
                font-weight: bold; border: 1px solid #3a3f4d; padding: 4px;
            }
            QPushButton { 
                background-color: #3a3f4d; color: white; 
                border-radius: 4px; padding: 6px 12px; border: none;
            }
            QPushButton:hover { background-color: #4e5568; }
            QGroupBox { 
                color: #00ff66; font-weight: bold; 
                border: 1px solid #3a3f4d; margin-top: 12px; padding-top: 15px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 頂部大標題
        title_label = QLabel("🖥️ 辦公室電腦遠端維護與排程控制中心")
        title_label.setFont(QFont("Microsoft JhengHei", 16, QFont.Bold))
        title_label.setStyleSheet("color: #00ff66; margin-bottom: 10px;")
        main_layout.addWidget(title_label)

        # 批次控制面板群組
        batch_group = QGroupBox("⚡ 全局批次控制 (10台電腦同時同步動作)")
        batch_layout = QHBoxLayout(batch_group)
        
        btn_batch_wol = QPushButton("☀️ 批次開機 (WOL)")
        btn_batch_wol.setStyleSheet("background-color: #27ae60; font-weight:bold; color:white;")
        btn_batch_wol.clicked.connect(lambda: self.trigger_batch_action("WOL"))
        
        btn_batch_shutdown = QPushButton("🌙 批次下班關機")
        btn_batch_shutdown.setStyleSheet("background-color: #c0392b; font-weight:bold; color:white;")
        btn_batch_shutdown.clicked.connect(lambda: self.trigger_batch_action("SHUTDOWN"))
        
        btn_batch_backup = QPushButton("📦 批次進入Linux執行自動備份")
        btn_batch_backup.setStyleSheet("background-color: #2980b9; font-weight:bold; color:white;")
        btn_batch_backup.clicked.connect(lambda: self.trigger_batch_action("ENTER_LINUX_BACKUP"))

        batch_layout.addWidget(btn_batch_wol)
        batch_layout.addWidget(btn_batch_shutdown)
        batch_layout.addWidget(btn_batch_backup)
        main_layout.addWidget(batch_group)

        # 電腦狀態清單表格
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["電腦名稱", "IP 位址", "MAC 位址 (WOL用)", "目前狀態", "最後操作結果", "單機控制動作"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents) # 操作欄配合按鈕大小
        main_layout.addWidget(self.table)

    def load_pc_list(self):
        """ 載入辦公室 10 台電腦的固定資訊，並優化 UI 畫面可讀性 """
        self.pc_data = [
            {"name": "OFFICE-PC01", "ip": "192.168.1.101", "mac": "70:8B:CD:12:34:56", "status": "在線"},
            {"name": "OFFICE-PC02", "ip": "192.168.1.102", "mac": "70:8B:CD:12:34:57", "status": "在線"},
            {"name": "OFFICE-PC03", "ip": "192.168.1.103", "mac": "70:8B:CD:12:34:58", "status": "離線"},
            {"name": "OFFICE-PC04", "ip": "192.168.1.104", "mac": "70:8B:CD:12:34:59", "status": "在線"},
            {"name": "OFFICE-PC05", "ip": "192.168.1.105", "mac": "70:8B:CD:12:34:5A", "status": "在線"},
            {"name": "OFFICE-PC06", "ip": "192.168.1.106", "mac": "70:8B:CD:12:34:5B", "status": "在線"},
            {"name": "OFFICE-PC07", "ip": "192.168.1.107", "mac": "70:8B:CD:12:34:5C", "status": "離線"},
            {"name": "OFFICE-PC08", "ip": "192.168.1.108", "mac": "70:8B:CD:12:34:5D", "status": "在線"},
            {"name": "OFFICE-PC09", "ip": "192.168.1.109", "mac": "70:8B:CD:12:34:5E", "status": "在線"},
            {"name": "OFFICE-PC10", "ip": "192.168.1.110", "mac": "70:8B:CD:12:34:5F", "status": "在線"},
        ]
        
        self.table.setRowCount(len(self.pc_data))
        
        # 💡 【關鍵修正 1】設定表格每一列的預設高度為 42 像素，徹底解決中文字被切掉的問題
        self.table.verticalHeader().setDefaultSectionSize(42)
        
        # 遍歷 10 台電腦資料並繪製 UI 表格
        for row, pc in enumerate(self.pc_data):
            self.table.setItem(row, 0, QTableWidgetItem(pc["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(pc["ip"]))
            self.table.setItem(row, 2, QTableWidgetItem(pc["mac"]))
            
            # 在線狀態顏色區分
            status_item = QTableWidgetItem(pc["status"])
            if pc["status"] == "在線":
                status_item.setForeground(QColor("#00ff66"))
            else:
                status_item.setForeground(QColor("#ff5555"))
            self.table.setItem(row, 3, status_item)
            
            # 初始化操作日誌欄位
            self.table.setItem(row, 4, QTableWidgetItem("等待指令..."))

            # 建立每台電腦獨立控制的按鈕容器
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(4, 2, 4, 2)  # 微調容器邊距
            btn_layout.setSpacing(6)                  # 增加按鈕之間的間距

            # 💡 【關鍵修正 2】優化按鈕樣式，縮減字型至 11px，並加上上下 padding 確保文字完美置中
            button_style = """
                QPushButton { 
                    background-color: #3a3f4d; color: white; 
                    border-radius: 4px; padding: 4px 8px; border: none;
                    font-size: 11px; font-weight: bold;
                }
                QPushButton:hover { background-color: #4e5568; }
            """

            btn_wol = QPushButton("開機")
            btn_wol.setStyleSheet(button_style)
            btn_wol.clicked.connect(lambda checked, r=row: self.trigger_single_action(r, "WOL"))
            
            btn_reboot = QPushButton("重啟")
            btn_reboot.setStyleSheet(button_style)
            btn_reboot.clicked.connect(lambda checked, r=row: self.trigger_single_action(r, "REBOOT"))
            
            # 💡 【關鍵修正 3】字串精簡為「Linux備份」，並套用藍色背景
            btn_linux = QPushButton("Linux備份")
            btn_linux.setStyleSheet(button_style + "QPushButton { background-color: #2980b9; } QPushButton:hover { background-color: #3498db; }")
            btn_linux.clicked.connect(lambda checked, r=row: self.trigger_single_action(r, "ENTER_LINUX_BACKUP"))

            btn_layout.addWidget(btn_wol)
            btn_layout.addWidget(btn_reboot)
            btn_layout.addWidget(btn_linux)
            
            self.table.setCellWidget(row, 5, btn_widget)


    # ==============================================================================
    # 3. 控制行為中樞邏輯
    # ==============================================================================
    def trigger_single_action(self, row, action):
        """ 觸發單台電腦的維護動作 """
        ip = self.table.item(row, 1).text()
        mac = self.table.item(row, 2).text()
        
        self.table.setItem(row, 4, QTableWidgetItem("命令傳送中..."))
        
        # 呼叫背景多執行緒，避免因網路阻擋或延遲導致管理工具主畫面卡死
        # 使用獨立變數保存 worker 參考，防止被垃圾回收
        setattr(self, f"worker_{row}", RemoteControlWorker(action, ip, mac))
        worker = getattr(self, f"worker_{row}")
        worker.status_signal.connect(lambda status_text: self.update_row_result(row, status_text))
        worker.start()

    def trigger_batch_action(self, action):
        """ 觸發全辦公室批次同步動作 """
        confirm = QMessageBox.question(
            self, "⚠️ 批次確認", 
            f"您確定要對辦公室【所有 10 台電腦】發送 {action} 指令嗎？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if confirm == QMessageBox.No:
            return

        # 批次循環調用單機控制邏輯
        for row in range(self.table.rowCount()):
            self.trigger_single_action(row, action)

    def update_row_result(self, row, status_text):
        """ 執行緒完成後，即時將網路結果更新回該電腦欄位 """
        self.table.setItem(row, 4, QTableWidgetItem(status_text))

# ==============================================================================
# 4. 程式啟動點
# ==============================================================================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft JhengHei", 10))
    console = AdminConsoleWindow()
    console.show()
    sys.exit(app.exec_())
