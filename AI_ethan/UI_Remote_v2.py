import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QListWidget, QInputDialog, QMessageBox)
from PyQt6.QtCore import Qt

class RemoteDesktopTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('IT 遠端桌面連線工具')
        self.resize(700, 400)
        
        # 主主要核心元件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # ==================== 左側：設備清單區 ====================
        left_layout = QVBoxLayout()
        
        list_title = QLabel('📑 設備 Profile 清單')
        list_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        left_layout.addWidget(list_title)
        
        self.device_list = QListWidget()
        # 預設範例資料 (格式: 名稱 | IP | 帳號)
        self.device_list.addItem("研發部-PC01 | 100.75.23.41 | Administrator")
        self.device_list.addItem("財務部-Server | 100.64.12.55 | admin")
        self.device_list.itemClicked.connect(self.load_profile)
        left_layout.addWidget(self.device_list)
        
        # 記憶清單按鈕
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton('💾 儲存目前輸入')
        self.btn_add.clicked.connect(self.save_profile)
        self.btn_del = QPushButton('❌ 刪除選取')
        self.btn_del.clicked.connect(self.delete_profile)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_del)
        left_layout.addLayout(btn_layout)
        
        # ==================== 右側：快速連線區 ====================
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)
        
        connect_title = QLabel('⚡ 快速連線設定 (支援外網VPN/Tailscale)')
        connect_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #2b579a;")
        right_layout.addWidget(connect_title)
        
        # IP 輸入
        right_layout.addWidget(QLabel('遠端主機 IP / 網域：'))
        self.txt_ip = QLineEdit()
        self.txt_ip.setPlaceholderText('例如: 100.75.23.41 或 ://domain.com')
        right_layout.addWidget(self.txt_ip)
        
        # 帳號輸入
        right_layout.addWidget(QLabel('使用者帳號：'))
        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText('例如: Administrator')
        right_layout.addWidget(self.txt_user)
        
        # 密碼輸入
        right_layout.addWidget(QLabel('連線密碼：'))
        self.txt_pwd = QLineEdit()
        self.txt_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_pwd.setPlaceholderText('請輸入遠端電腦密碼')
        right_layout.addWidget(self.txt_pwd)
        
        # 彈性伸展空間
        right_layout.addStretch()
        
        # 登入按鈕
        self.btn_connect = QPushButton('⚡ 立即安全登入远端')
        self.btn_connect.setStyleSheet("""
            QPushButton {
                background-color: #2b579a; 
                color: white; 
                font-size: 16px; 
                font-weight: bold; 
                padding: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1e3f73;
            }
        """)
        self.btn_connect.clicked.connect(self.action_connect)
        right_layout.addWidget(self.btn_connect)
        
        # 將左右佈局放入主畫面
        main_layout.addLayout(left_layout, stretch=4)
        main_layout.addLayout(right_layout, stretch=6)

    # ==================== 功能邏輯控制 ====================
    def load_profile(self, item):
        """點擊清單時，自動填入右側輸入框"""
        try:
            parts = item.text().split(" | ")
            if len(parts) == 3:
                self.txt_ip.setText(parts[1])
                self.txt_user.setText(parts[2])
                self.txt_pwd.clear()  # 基於資安，不儲存密碼，由工程師現場輸入
                self.txt_pwd.setFocus()
        except Exception as e:
            pass

    def save_profile(self):
        """修正原第180行錯誤：使用正確的 QInputDialog 彈出視窗"""
        ip = self.txt_ip.text().strip()
        user = self.txt_user.text().strip()
        
        if not ip or not user:
            QMessageBox.warning(self, '提示', '請先輸入 IP 與 帳號再進行儲存！')
            return
            
        # 這裡就是原本第 180 行的位置，已修正為 PyQt6 正確語法
        name, ok = QInputDialog.getText(self, '儲存 Profile', '請輸入此設備的辨識名稱：')
        
        if ok and name.strip():
            profile_string = f"{name.strip()} | {ip} | {user}"
            self.device_list.addItem(profile_string)
            QMessageBox.information(self, '成功', f'Profile [{name}] 已儲存！')

    def delete_profile(self):
        """刪除選中的 Profile"""
        current_row = self.device_list.currentRow()
        if current_row >= 0:
            self.device_list.takeItem(current_row)
        else:
            QMessageBox.warning(self, '提示', '請先選擇要刪除的項目。')

    def action_connect(self):
        """執行 RDP 安全連線"""
        ip = self.txt_ip.text().strip()
        user = self.txt_user.text().strip()
        pwd = self.txt_pwd.text().strip()
        
        if not ip or not user or not pwd:
            QMessageBox.warning(self, '欄位缺失', 'IP、帳號與密碼皆為必填項目！')
            return
            
        try:
            # 1. 注入認證管理員
            cred_cmd = f"cmdkey /generic:TERMSRV/{ip} /user:{user} /pass:{pwd}"
            subprocess.run(cred_cmd, shell=True, check=True)
            
            # 2. 啟動內建遠端桌面
            self.statusBar().showMessage(f"連線中: {ip}...")
            subprocess.run(f"mstsc /v:{ip} /f", shell=True)
            
        except Exception as e:
            QMessageBox.critical(self, '連線失敗', f'無法建立連線:\n{str(e)}')
        finally:
            # 3. 清除安全憑據
            clear_cmd = f"cmdkey /delete:TERMSRV/{ip}"
            subprocess.run(clear_cmd, shell=True)
            self.statusBar().showMessage("連線已關閉，安全憑據已清除。")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RemoteDesktopTool()
    ex.show()
    # 修正 exec__ 錯誤，PyQt6 統一使用新版標準 exec()
    sys.exit(app.exec())
