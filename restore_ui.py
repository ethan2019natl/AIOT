import sys
import time
import re
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QComboBox, QListWidget, 
                             QPushButton, QProgressBar, QTextEdit, QCheckBox, 
                             QMessageBox, QFrame, QSplitter)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

# ==========================================
# 1. 後端還原執行緒 (預防介面卡死並解析進度)
# ==========================================
class RestoreWorker(QThread):
    progress_signal = pyqtSignal(int)
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, source_img, target_disk):
        super().__init__()
        self.source_img = source_img
        self.target_disk = target_disk

    def run(self):
        try:
            # 實際部署時的 Linux 還原指令範例 (解壓 zstd 並透過 partclone 還原)
            # cmd = f"zstd -d -c {self.source_img} | partclone.ntfs -r -d -o {self.target_disk}"
            
            # 以下為模擬 partclone 輸出的測試程式碼 (實際開發時切換回上方真實指令)
            self.log_signal.emit(f"[資訊] 開始還原流程...")
            self.log_signal.emit(f"[來源] {self.source_img}")
            self.log_signal.emit(f"[目的] {self.target_disk}\n")
            
            for i in range(1, 101):
                time.sleep(0.05)  # 模擬封裝還原耗時
                self.progress_signal.emit(i)
                self.log_signal.emit(f"Calculating disk clusters... Syncing... {i}.00% completed.")
            
            self.finished_signal.emit(True, "系統還原成功！請重新開機。")
        except Exception as e:
            self.finished_signal.emit(False, str(e))

# ==========================================
# 2. 前端還原主畫面 UI
# ==========================================
class RestoreWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_mock_data()  # 載入模擬資料 (實務上改為讀取 E 碟與 NAS 檔案)

    def initUI(self):
        # 視窗基本設定
        self.setWindowTitle("企業電腦維護系統 - 離線還原工具 (Linux 環境)")
        self.resize(1000, 650)
        self.setMinimumSize(850, 550)
        
        # 主樣式表 (深色調/科技感，適合維護人員使用)
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e24; }
            QLabel { color: #ffffff; font-size: 14px; }
            QComboBox, QListWidget, QTextEdit { 
                background-color: #2a2a32; 
                color: #ffffff; 
                border: 1px solid #4a4a5a; 
                border-radius: 4px;
                padding: 5px;
            }
            QComboBox::drop-down { border: none; }
            QListWidget::item:selected { background-color: #007acc; }
            QProgressBar { 
                background-color: #2a2a32; 
                color: white; 
                text-align: center; 
                border-radius: 5px; 
                border: 1px solid #4a4a5a;
            }
            QProgressBar::chunk { background-color: #007acc; width: 10px; }
            QCheckBox { color: #ff5555; font-weight: bold; }
        """)

        # 主集中控制元件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # ================= 🔧 左側控制面板 =================
        left_panel = QFrame()
        left_panel.setFixedWidth(400)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(15)

        # 1. 選擇備份來源儲存區
        source_label = QLabel("📁 步驟一：選擇鏡像檔來源")
        source_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.combo_source_type = QComboBox()
        self.combo_source_type.addItems(["本機 E 磁碟 (高效率保存區)", "公司 NAS 伺服器 [每月排程備份]"])
        self.combo_source_type.currentIndexChanged.connect(self.on_source_type_changed)

        # 2. 備份版本清單
        version_label = QLabel("📅 步驟二：點選還原版本 (.img)")
        self.list_versions = QListWidget()
        
        # 3. 選擇目的地磁碟 (防呆確認)
        target_label = QLabel("💽 步驟三：選擇還原目的磁碟")
        self.combo_target_disk = QComboBox()

        # 4. 安全鎖與執行按鈕
        self.check_safety = QCheckBox(" 我已知曉此操作將完全覆蓋該磁碟所有資料")
        self.check_safety.stateChanged.connect(self.on_safety_changed)

        self.btn_start = QPushButton("🚀 開始系統還原")
        self.btn_start.setEnabled(False) # 初始鎖定
        self.btn_start.setFont(QFont("Arial", 12, QFont.Bold))
        self.btn_start.setStyleSheet("""
            QPushButton { 
                background-color: #44444c; color: #888888; 
                border-radius: 5px; padding: 12px; border: none;
            }
            QPushButton:enabled { background-color: #d9534f; color: white; }
            QPushButton:enabled:hover { background-color: #c9302c; }
        """)
        self.btn_start.clicked.connect(self.start_restore_process)

        # 組合左側布局
        left_layout.addWidget(source_label)
        left_layout.addWidget(self.combo_source_type)
        left_layout.addWidget(version_label)
        left_layout.addWidget(self.list_versions)
        left_layout.addWidget(target_label)
        left_layout.addWidget(self.combo_target_disk)
        left_layout.addWidget(self.check_safety)
        left_layout.addWidget(self.btn_start)

        # ================= 📊 右側日誌與進度面板 =================
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)

        log_label = QLabel("📋 即時還原狀態與 partclone 日誌")
        log_label.setFont(QFont("Arial", 12, QFont.Bold))
        
        self.txt_logs = QTextEdit()
        self.txt_logs.setReadOnly(True)
        self.txt_logs.setFont(QFont("Courier New", 10))

        progress_label = QLabel("⌛ 整體還原進度：")
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")

        # 組合右側布局
        right_layout.addWidget(log_label)
        right_layout.addWidget(self.txt_logs)
        right_layout.addWidget(progress_label)
        right_layout.addWidget(self.progress_bar)

        # ================= 視窗左右拼接 =================
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(1, 2) # 右側日誌區寬度比例較大
        
        main_layout.addWidget(splitter)

    # ==========================================
    # 3. 前端 UI 邏輯控制與防呆
    # ==========================================
    def load_mock_data(self):
        """模擬從系統撈取磁碟代號與 NAS 檔案清單"""
        # 模擬本機 E 碟讀到的備份檔
        self.mock_local_images = [
            "PC01_C_Drive_20260824_Full.img",
            "PC01_D_Drive_20260824_Data.img",
            "PC01_C_Drive_20260701_Stable.img"
        ]
        # 模擬 NAS 讀到的遠端備份檔
        self.mock_nas_images = [
            "NAS_Backup_PC01_C_20260801.img",
            "NAS_Backup_PC01_D_20260801.img"
        ]
        
        # 預設載入本機備份清單
        self.list_versions.addItems(self.mock_local_images)

        # 模擬偵測到的 Linux 下 Windows 磁碟代號 (實務上透過 lsblk --json 抓取)
        self.combo_target_disk.addItem("請選擇目的分割區...", None)
        self.combo_target_disk.addItem("/dev/nvme0n1p2 (Windows C: 系統碟 120GB)", "/dev/nvme0n1p2")
        self.combo_target_disk.addItem("/dev/nvme0n1p3 (Windows D: 資料碟 350GB)", "/dev/nvme0n1p3")

    def on_source_type_changed(self, index):
        """當切換本機 E 碟或 NAS 時，連動更新版本檔案清單"""
        self.list_versions.clear()
        if index == 0:
            self.list_versions.addItems(self.mock_local_images)
            self.txt_logs.append("[系統提示] 已切換讀取來源：本機 E 碟。")
        else:
            self.list_versions.addItems(self.mock_nas_images)
            self.txt_logs.append("[系統提示] 已切換讀取來源：公司 NAS 遠端伺服器。")

    def on_safety_changed(self, state):
        """防呆核取方塊控制：勾選後按鈕才亮起"""
        self.btn_start.setEnabled(state == Qt.Checked)

    def start_restore_process(self):
        """開始還原按鈕事件"""
        selected_img = self.list_versions.currentItem()
        target_data = self.combo_target_disk.currentData()

        # 驗證是否有選取檔案與磁碟
        if not selected_img:
            QMessageBox.warning(self, "錯誤", "請先從清單中點選一個備份鏡像檔 (.img)！")
            return
        if not target_data:
            QMessageBox.warning(self, "錯誤", "請選擇正確的還原目的磁碟區！")
            return

        # 二次彈窗警告
        reply = QMessageBox.question(
            self, '⚠️ 終極確認', 
            f"確定要將【{selected_img.text()}】\n還原至【{self.combo_target_disk.currentText()}】嗎？\n該分割區所有資料將灰飛煙滅！",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # 鎖定 UI 避免還原中途被亂點選
            self.btn_start.setEnabled(False)
            self.check_safety.setEnabled(False)
            self.combo_source_type.setEnabled(False)
            self.list_versions.setEnabled(False)
            self.combo_target_disk.setEnabled(False)
            
            # 啟動後端子執行緒進行還原
            self.worker = RestoreWorker(selected_img.text(), target_data)
            self.worker.progress_signal.connect(self.progress_bar.setValue)
            self.worker.log_signal.connect(self.txt_logs.append)
            self.worker.finished_signal.connect(self.on_restore_finished)
            self.worker.start()

    def on_restore_finished(self, success, message):
        """當還原完成或失敗時的回呼函數"""
        if success:
            QMessageBox.information(self, "還原完成", message)
            self.txt_logs.append("\n[成功] 系統還原作業已全數完成。")
        else:
            QMessageBox.critical(self, "系統失敗", f"還原終止，原因：{message}")
            self.txt_logs.append(f"\n[錯誤] 還原失敗：{message}")
            
        # 解鎖 UI 介面
        self.check_safety.setChecked(False)
        self.check_safety.setEnabled(True)
        self.combo_source_type.setEnabled(True)
        self.list_versions.setEnabled(True)
        self.combo_target_disk.setEnabled(True)

# ==========================================
# 4. 程式進入點
# ==========================================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RestoreWindow()
    window.show()
    sys.exit(app.exec_())
