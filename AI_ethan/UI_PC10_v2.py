import sys
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTableWidget, QTableWidgetItem, 
                             QPushButton, QLabel, QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor

# 模擬 10 台辦公室電腦資料
COMPUTERS_DATA = [
    {"id": f"PC-{i:02d}", "ip": f"192.168.1.{10+i}", "os": "Windows 11", "status": "檢測中..."}
    for i in range(1, 11)
]

# 後台執行緒：負責檢查 10 台電腦的 Ping 狀態，避免 UI 卡死
class StatusCheckThread(QThread):
    status_updated = pyqtSignal(int, str)  # 傳回 (行數, 狀態字串)

    def run(self):
        while True:
            for row, pc in enumerate(COMPUTERS_DATA):
                # 實際環境請替換為真實的 ping 指令
                # status = "在線" if os.system(f"ping -c 1 {pc['ip']}") == 0 else "離線"
                time.sleep(0.1)  # 模擬網路延遲
                status = "在線" if row % 3 != 0 else "離線" # 模擬部分離線
                self.status_updated.emit(row, status)
            time.sleep(5)  # 每 5 秒更新一次狀態

class RemoteManagerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # 啟動狀態監控執行緒
        self.status_thread = StatusCheckThread()
        self.status_thread.status_updated.connect(self.update_pc_status)
        self.status_thread.start()

    def initUI(self):
        self.setWindowTitle('企業內部遠端連線整合管理工具 (10台主機)')
        self.resize(900, 500)
        self.setStyleSheet("background-color: #f5f6fa;")

        # 主佈局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 標題列
        title_label = QLabel("遠端電腦電源與備份分區管理面板")
        title_label.setFont(QFont("Microsoft JhengHei", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2f3640; margin: 10px 0px;")
        main_layout.addWidget(title_label)

        # 電腦列表表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["電腦名稱", "IP 位址", "目前作業系統", "即時狀態", "維護操作"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #353b48; color: white; font-weight: bold; }")
        self.table.setRowCount(len(COMPUTERS_DATA))
        
        # 填入初始資料
        for row, pc in enumerate(COMPUTERS_DATA):
            self.table.setItem(row, 0, QTableWidgetItem(pc["id"]))
            self.table.setItem(row, 1, QTableWidgetItem(pc["ip"]))
            self.table.setItem(row, 2, QTableWidgetItem(pc["os"]))
            
            status_item = QTableWidgetItem(pc["status"])
            status_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, status_item)

            # 操作按鈕欄位 (放置綜合控制按鈕)
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(5, 2, 5, 2)
            btn_layout.setSpacing(5)

            # 建立個別動作按鈕
            btn_linux = QPushButton("切換Linux分區")
            btn_linux.setStyleSheet("background-color: #e1b12c; color: white; border-radius: 3px; padding: 3px;")
            btn_linux.clicked.connect(lambda checked, r=row: self.handle_action(r, "boot_linux"))

            btn_backup = QPushButton("備份/還原")
            btn_backup.setStyleSheet("background-color: #44bd32; color: white; border-radius: 3px; padding: 3px;")
            btn_backup.clicked.connect(lambda checked, r=row: self.handle_action(r, "backup_restore"))

            btn_layout.addWidget(btn_linux)
            btn_layout.addWidget(btn_backup)
            self.table.setCellWidget(row, 4, btn_widget)

        main_layout.addWidget(self.table)

        # 全局控制底部工具列
        bottom_layout = QHBoxLayout()
        lbl_global = QLabel("全域批次操作：")
        lbl_global.setFont(QFont("Microsoft JhengHei", 10, QFont.Bold))
        
        btn_all_on = QPushButton("全部開機 (WOL)")
        btn_all_on.setStyleSheet("background-color: #0097e6; color: white; padding: 8px 15px; font-weight: bold;")
        btn_all_on.clicked.connect(lambda: self.global_action("全部開機"))

        btn_all_off = QPushButton("全部關機")
        btn_all_off.setStyleSheet("background-color: #c23616; color: white; padding: 8px 15px; font-weight: bold;")
        btn_all_off.clicked.connect(lambda: self.global_action("全部關機"))

        btn_all_reboot = QPushButton("全部重啟")
        btn_all_reboot.setStyleSheet("background-color: #718093; color: white; padding: 8px 15px; font-weight: bold;")
        btn_all_reboot.clicked.connect(lambda: self.global_action("全部重啟"))

        bottom_layout.addWidget(lbl_global)
        bottom_layout.addWidget(btn_all_on)
        bottom_layout.addWidget(btn_all_off)
        bottom_layout.addWidget(btn_all_reboot)
        bottom_layout.addStretch()

        main_layout.addLayout(bottom_layout)

    # 更新狀態燈號與文字
    def update_pc_status(self, row, status):
        status_item = self.table.item(row, 3)
        status_item.setText(status)
        if status == "在線":
            status_item.setForeground(QColor("#44bd32")) # 綠色
        else:
            status_item.setForeground(QColor("#718093")) # 灰色

    # 處理個別電腦的操作
    def handle_action(self, row, action_type):
        pc_id = self.table.item(row, 0).text()
        ip = self.table.item(row, 1).text()
        
        if action_type == "boot_linux":
            # 這裡實作遠端修改 GRUB 或透過 WinRM 執行下一次啟動進入 Linux
            QMessageBox.information(self, "指令發送", f"已向 {pc_id} ({ip}) 發送指令：\n修改開機選單，重啟並進入 Linux 啟動分區。")
            self.table.item(row, 2).setText("Linux (救援分區)")
        
        elif action_type == "backup_restore":
            current_os = self.table.item(row, 2).text()
            if "Linux" not in current_os:
                QMessageBox.warning(self, "權限錯誤", f"{pc_id} 目前不在 Linux 分區內，無法進行獨立分割區備份！\n請先點擊『切換Linux分區』。")
                return
            # 呼叫後台 Linux 伺服器的 Clonezilla / rsync 腳本
            QMessageBox.information(self, "備份程序", f"已啟動 {pc_id} 的 Linux 環境備份程序...\n映像檔將同步至中央 Linux 伺服器儲存池。")

    # 處理全域操作
    def global_action(self, action_name):
        reply = QMessageBox.question(self, '確認操作', f'您確定要對辦公室內所有 10 台電腦執行【{action_name}】嗎？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 迴圈呼叫網路喚醒(WOL)或 WinRM 關機指令
            QMessageBox.information(self, "執行中", f"正在批次執行：{action_name}...")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RemoteManagerUI()
    ex.show()
    sys.exit(app.exec())

