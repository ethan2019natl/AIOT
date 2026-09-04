import sys
import os
import subprocess
import time
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QListWidget, QInputDialog, QMessageBox, QGroupBox)
from PyQt6.QtCore import Qt

# 定義設定檔儲存路徑（與程式放在同一個資料夾）
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

class PiJumpBoxRemoteTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_settings_from_json() # 啟動時自動讀取設定
        
    def initUI(self):
        self.setWindowTitle('IT 樹梅派跳板遠端管理工具 (LAN 10台)')
        self.resize(800, 480)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # ==================== 左側：10台電腦設備清單 ====================
        left_layout = QVBoxLayout()
        
        list_title = QLabel('📑 辦公室區域網路設備 (LAN)')
        list_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        left_layout.addWidget(list_title)
        
        self.device_list = QListWidget()
        self.device_list.itemClicked.connect(self.load_profile)
        left_layout.addWidget(self.device_list)
        
        # 自訂管理按鈕
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton('➕ 新增設備')
        self.btn_add.clicked.connect(self.save_profile)
        self.btn_del = QPushButton('❌ 刪除設備')
        self.btn_del.clicked.connect(self.delete_profile)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_del)
        left_layout.addLayout(btn_layout)
        
        # ==================== 右側：跳板機與目標設定 ====================
        right_layout = QVBoxLayout()
        right_layout.setSpacing(8)
        
        # ---- 區塊 1：樹梅派跳板機設定 (SSH) ----
        pi_group = QGroupBox("🍓 樹梅派跳板機設定 (堡壘機)")
        pi_group.setStyleSheet("QGroupBox { font-weight: bold; color: #d32f2f; }")
        pi_box = QVBoxLayout()
        
        pi_box.addWidget(QLabel('樹梅派 外網IP / 網域 / Tailscale IP：'))
        self.txt_pi_ip = QLineEdit()
        self.txt_pi_ip.setPlaceholderText('例如: 100.115.24.85')
        pi_box.addWidget(self.txt_pi_ip)
        
        pi_user_layout = QHBoxLayout()
        pi_user_layout.addWidget(QLabel('SSH 帳號:'))
        self.txt_pi_user = QLineEdit()
        pi_user_layout.addWidget(self.txt_pi_user)
        
        pi_user_layout.addWidget(QLabel('SSH 密碼(選填):'))
        self.txt_pi_pwd = QLineEdit()
        self.txt_pi_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_pi_pwd.setPlaceholderText('留空則使用SSH Key')
        pi_user_layout.addWidget(self.txt_pi_pwd)
        pi_box.addLayout(pi_user_layout)
        
        pi_group.setLayout(pi_box)
        right_layout.addWidget(pi_group)
        
        # ---- 區塊 2：目標 Windows 電腦設定 ----
        win_group = QGroupBox("💻 目標 Windows 電腦 (辦公室內網)")
        win_group.setStyleSheet("QGroupBox { font-weight: bold; color: #2b579a; }")
        win_box = QVBoxLayout()
        
        win_box.addWidget(QLabel('區域網路內部 IP：'))
        self.txt_win_ip = QLineEdit()
        self.txt_win_ip.setPlaceholderText('例如: 192.168.1.11')
        win_box.addWidget(self.txt_win_ip)
        
        win_acc_layout = QHBoxLayout()
        win_acc_layout.addWidget(QLabel('登入帳號:'))
        self.txt_win_user = QLineEdit()
        win_acc_layout.addWidget(self.txt_win_user)
        
        win_acc_layout.addWidget(QLabel('登入密碼:'))
        self.txt_win_pwd = QLineEdit()
        self.txt_win_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        win_box.addLayout(win_acc_layout)
        
        win_group.setLayout(win_box)
        right_layout.addWidget(win_group)
        
        right_layout.addStretch()
        
        # ---- 連線按鈕 ----
        self.btn_connect = QPushButton('⚡ 透過樹梅派建立安全連線')
        self.btn_connect.setStyleSheet("""
            QPushButton {
                background-color: #2b579a; color: white; 
                font-size: 15px; font-weight: bold; padding: 12px; border-radius: 5px;
            }
            QPushButton:hover { background-color: #1e3f73; }
        """)
        self.btn_connect.clicked.connect(self.action_connect)
        right_layout.addWidget(self.btn_connect)
        
        main_layout.addLayout(left_layout, stretch=4)
        main_layout.addLayout(right_layout, stretch=6)

    # ==================== JSON 檔案讀寫邏輯 ====================
    def load_settings_from_json(self):
        """從 JSON 檔案載入設定，若檔案不存在則建立預設值"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # 載入樹梅派設定
                self.txt_pi_ip.setText(data.get("pi_ip", ""))
                self.txt_pi_user.setText(data.get("pi_user", ""))
                
                # 載入設備清單
                devices = data.get("devices", [])
                self.device_list.addItems(devices)
                return
            except Exception as e:
                print(f"讀取 JSON 失敗，將載入預設值: {e}")

        # 若無檔案或讀取失敗，載入預設的 10 台範例資料
        default_devices = [
            "辦公室-PC01 | 192.168.1.11 | Administrator",
            "辦公室-PC02 | 192.168.1.12 | Administrator",
            "辦公室-PC03 | 192.168.1.13 | User",
            "財務部-專用機 | 192.168.1.20 | admin",
            "主管-Laptop | 192.168.1.30 | Administrator",
            "會議室-Projector | 192.168.1.40 | Guest",
            "備用機-PC07 | 192.168.1.17 | Administrator",
            "備用機-PC08 | 192.168.1.18 | Administrator",
            "NAS-儲存伺服器 | 192.168.1.200 | admin",
            "門市-POS終端 | 192.168.1.99 | pos_user"
        ]
        self.device_list.addItems(default_devices)
        self.txt_pi_ip.setText("100.115.24.85")
        self.txt_pi_user.setText("pi")
        self.save_settings_to_json() # 順便建立初始檔案

    def save_settings_to_json(self):
        """將目前介面上的設定儲存至 JSON 檔案"""
        # 收集清單內所有項目
        devices = []
        for i in range(self.device_list.count()):
            devices.append(self.device_list.item(i).text())
            
        data = {
            "pi_ip": self.txt_pi_ip.text().strip(),
            "pi_user": self.txt_pi_user.text().strip(),
            "devices": devices
        }
        
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"儲存 JSON 失敗: {e}")

    def closeEvent(self, event):
        """當使用者關閉視窗時，自動觸發儲存"""
        self.save_settings_to_json()
        event.accept()

    # ==================== 介面按鈕功能 ====================
    def load_profile(self, item):
        try:
            parts = item.text().split(" | ")
            if len(parts) == 3:
                self.txt_win_ip.setText(parts[1])
                self.txt_win_user.setText(parts[2])
                self.txt_win_pwd.clear()
                self.txt_win_pwd.setFocus()
        except Exception:
            pass

    def save_profile(self):
        ip = self.txt_win_ip.text().strip()
        user = self.txt_win_user.text().strip()
        if not ip or not user:
            QMessageBox.warning(self, '提示', '請先填寫 Windows IP 與 帳號')
            return
        name, ok = QInputDialog.getText(self, '新增設備', '請輸入設備辨識名稱：')
        if ok and name.strip():
            self.device_list.addItem(f"{name.strip()} | {ip} | {user}")
            self.save_settings_to_json() # 新增後立即存檔

    def delete_profile(self):
        current_row = self.device_list.currentRow()
        if current_row >= 0:
            self.device_list.takeItem(current_row)
            self.save_settings_to_json() # 刪除後立即存檔
        else:
            QMessageBox.warning(self, '提示', '請先選擇要刪除的項目。')

    def action_connect(self):
        self.save_settings_to_json() # 連線前也自動存檔一次
        
        pi_ip = self.txt_pi_ip.text().strip()
        pi_user = self.txt_pi_user.text().strip()
        
        win_ip = self.txt_win_ip.text().strip()
        win_user = self.txt_win_user.text().strip()
        win_pwd = self.txt_win_pwd.text().strip()
        
        if not all([pi_ip, pi_user, win_ip, win_user, win_pwd]):
            QMessageBox.warning(self, '欄位缺失', '請確認樹梅派設定與 Windows 帳密皆已輸入！')
            return

        local_port = "13389"
        
        try:
            self.statusBar().showMessage("正在打通樹梅派安全隧道...")
            
            # 1. 注入 RDP 憑據
            cred_cmd = f"cmdkey /generic:TERMSRV/localhost:{local_port} /user:{win_user} /pass:{win_pwd}"
            subprocess.run(cred_cmd, shell=True, check=True)
            
            # 2. 建立 SSH 隧道
            tunnel_start_cmd = f"start /B ssh -o StrictHostKeyChecking=no -N -L {local_port}:{win_ip}:3389 {pi_user}@{pi_ip}"
            subprocess.run(tunnel_start_cmd, shell=True)
            
            time.sleep(2)
            
            # 3. 開啟遠端桌面
            self.statusBar().showMessage(f"已穿透樹梅派！正在連線至區網 Windows: {win_ip}")
            subprocess.run(f"mstsc /v:localhost:{local_port} /f", shell=True)
            
        except Exception as e:
            QMessageBox.critical(self, '連線失敗', f'穿透失敗:\n{str(e)}')
        finally:
            # 4. 清理環境
            subprocess.run(f"cmdkey /delete:TERMSRV/localhost:{local_port}", shell=True)
            subprocess.run("taskkill /IM ssh.exe /F", shell=True)
            self.statusBar().showMessage("安全隧道已關閉，安全憑據已清除。")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PiJumpBoxRemoteTool()
    ex.show()
    sys.exit(app.exec())
