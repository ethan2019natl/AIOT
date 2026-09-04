import sys
import os
import subprocess
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QListWidget, QInputDialog, QMessageBox, QGroupBox)
from PyQt6.QtCore import Qt

class PiJumpBoxRemoteTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tunnel_process = None # 用於追蹤 SSH 隧道進程
        self.initUI()
        
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
        # 預先內建該辦公室的 10 台常用電腦設定 (名稱 | 區網IP | 帳號)
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
        self.device_list.itemClicked.connect(self.load_profile)
        left_layout.addWidget(self.device_list)
        
        # 自訂管理按鈕
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton('➕ 新增')
        self.btn_add.clicked.connect(self.save_profile)
        self.btn_del = QPushButton('❌ 刪除')
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
        self.txt_pi_ip.setText('100.115.24.85') # 可填入樹梅派的固定IP或VPN IP
        pi_box.addWidget(self.txt_pi_ip)
        
        pi_user_layout = QHBoxLayout()
        pi_user_layout.addWidget(QLabel('SSH 帳號:'))
        self.txt_pi_user = QLineEdit()
        self.txt_pi_user.setText('pi') # 樹梅派預設通常是 pi
        pi_user_layout.addWidget(self.txt_pi_user)
        
        pi_user_layout.addWidget(QLabel('SSH 密碼:'))
        self.txt_pi_pwd = QLineEdit()
        self.txt_pi_pwd.setEchoMode(QLineEdit.EchoMode.Password)
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
        win_acc_layout.addWidget(self.txt_win_pwd)
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
        
        # 組合左右排版
        main_layout.addLayout(left_layout, stretch=4)
        main_layout.addLayout(right_layout, stretch=6)

    # ==================== 功能邏輯 ====================
    def load_profile(self, item):
        """點擊左側清單，自動填入右側 Windows 欄位"""
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

    def delete_profile(self):
        current_row = self.device_list.currentRow()
        if current_row >= 0:
            self.device_list.takeItem(current_row)

    def action_connect(self):
        """核心技術：透過 SSH 隧道穿透區網進行 RDP 連線"""
        pi_ip = self.txt_pi_ip.text().strip()
        pi_user = self.txt_pi_user.text().strip()
        pi_pwd = self.txt_pi_pwd.text().strip()
        
        win_ip = self.txt_win_ip.text().strip()
        win_user = self.txt_win_user.text().strip()
        win_pwd = self.txt_win_pwd.text().strip()
        
        if not all([pi_ip, pi_user, win_ip, win_user, win_pwd]):
            QMessageBox.warning(self, '欄位缺失', '請確認樹梅派設定與 Windows 帳密皆已輸入！')
            return

        # 這裡定義本地端對應的映射埠號 (避免衝突使用 13389)
        local_port = "13389"
        
        try:
            self.statusBar().showMessage("正在打通樹梅派安全隧道...")
            
            # 使用 Windows 內建 OpenSSH 客戶端建立背景隧道 (L 參數負責埠口轉發)
            # 指令邏輯：把本機的 13389 透過樹梅派，對接到區網 Windows 的 3389 埠
            # 備註：若樹梅派密碼包含特殊字元，實務上建議使用 SSH Key 免密登入更穩定。
            # 這裡採用 Windows 支援的 ssh 語法環境
            ssh_tunnel_cmd = f"ssh -N -L {local_port}:{win_ip}:3389 {pi_user}@{pi_ip}"
            
            # 使用 plink (Putty 家族工具) 或 Windows 內建 ssh。這裡為了簡潔直接叫用背景進程
            # 注意：這裡假設管理員本機已與樹梅派建立過信任關係(或使用Key)，若需自動帶密碼，通常會搭配 sshpass 或 putty/plink
            # 為確保體驗流暢，我們這裡用標準 mstsc 流程。
            
            # 1. 注入認證資訊至本地端的 13389 埠 (對應 localhost)
            cred_cmd = f"cmdkey /generic:TERMSRV/localhost:{local_port} /user:{win_user} /pass:{win_pwd}"
            subprocess.run(cred_cmd, shell=True, check=True)
            
            # 2. 在背景啟動 SSH 隧道（需要手動在彈出視窗輸入一次樹梅派密碼，或是已設定免密密鑰）
            # 提示：最完美的自動化方式是請管理員將本機公鑰(id_rsa.pub)放進樹梅派中
            tunnel_start_cmd = f"start /B ssh -o StrictHostKeyChecking=no -N -L {local_port}:{win_ip}:3389 {pi_user}@{pi_ip}"
            subprocess.run(tunnel_start_cmd, shell=True)
            
            # 稍微等待 2 秒讓隧道建立完畢
            time.sleep(2)
            
            # 3. 呼叫遠端桌面主機連線到本地對應埠
            self.statusBar().showMessage(f"已穿透樹梅派！正在連線至區網 Windows: {win_ip}")
            subprocess.run(f"mstsc /v:localhost:{local_port} /f", shell=True)
            
        except Exception as e:
            QMessageBox.critical(self, '連線失敗', f'穿透失敗:\n{str(e)}')
        finally:
            # 4. 安全清理：關閉遠端桌面後，清除認證與關閉 SSH 隧道
            subprocess.run(f"cmdkey /delete:TERMSRV/localhost:{local_port}", shell=True)
            subprocess.run("taskkill /IM ssh.exe /F", shell=True) # 關閉背景 SSH 進程
            self.statusBar().showMessage("安全隧道已關閉，安全憑據已清除。")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PiJumpBoxRemoteTool()
    ex.show()
    sys.exit(app.exec())
