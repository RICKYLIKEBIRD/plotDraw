from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QListWidget, QSizePolicy, 
    QFormLayout, QWidget, QComboBox
)
from PyQt5.QtCore import Qt
import re
from qtwidgets import AnimatedToggle

class CsvReaderGui:
    def setup_gui(self):
        self.setWindowTitle("CSV讀取器")
        self.setGeometry(100, 100, 600, 300)

        self.main_layout = QHBoxLayout()

        self.left_layout = QVBoxLayout()
        
        #固定左側面板不被拉伸
        self.left_layout_container = QWidget()
        self.left_layout_container.setLayout(self.left_layout)
        self.left_layout_container.setMaximumWidth(300)  # 設定最大寬度
        
        self.main_layout.addWidget(self.left_layout_container)

        self.open_button = QPushButton("打開CSV檔案")
        self.open_button.clicked.connect(self.open_csv)
        self.left_layout.addWidget(self.open_button)

        self.label_and_button_layout = QHBoxLayout()
        
        self.all_setting_label = QLabel("是否啟用統一設定")
        self.all_setting_label.setStyleSheet("font-weight: bold;")
        self.all_setting_label.setFixedWidth(135)
        self.label_and_button_layout.addWidget(self.all_setting_label)
        
        self.enable_button = AnimatedToggle(checked_color="#FFB000",pulse_checked_color="#44FFB000")
        self.enable_button.setFixedWidth(60)  # 設定按鈕的寬度
        self.enable_button.clicked.connect(self.test)
        
        self.label_and_button_layout.addWidget(self.enable_button)
        self.label_and_button_layout.setAlignment(self.all_setting_label, Qt.AlignLeft)
        self.label_and_button_layout.setAlignment(self.enable_button, Qt.AlignLeft)
        
        self.left_layout.addLayout(self.label_and_button_layout)

        self.axis_selectors_layout = QFormLayout()  # 在此處添加 axis_selectors_layout
        self.left_layout.addLayout(self.axis_selectors_layout)

        self.x_title_label = QLabel("自定義X軸標題：")
        self.left_layout.addWidget(self.x_title_label)

        self.x_title_input = QLineEdit()
        self.left_layout.addWidget(self.x_title_input)

        self.y_title_label = QLabel("自定義Y軸標題：")
        self.left_layout.addWidget(self.y_title_label)
        
        self.y_title_input = QLineEdit()
        self.left_layout.addWidget(self.y_title_input)
        
        self.x_selector_label = QLabel("X軸資料:")
        self.x_axis_selector = QComboBox()
        self.x_selector_layout = QHBoxLayout()
        
        self.x_axis_selector.setFixedWidth(200)
        self.x_axis_selector.setEnabled(False)
        
        self.x_selector_layout.addWidget(self.x_selector_label)
        self.x_selector_layout.addWidget(self.x_axis_selector)
        self.left_layout.addLayout(self.x_selector_layout)
        
        self.y_selector_label = QLabel("Y軸資料:")
        self.y_axis_selector = QComboBox()
        self.y_selector_layout = QHBoxLayout()
        
        self.y_axis_selector.setFixedWidth(200)
        self.y_axis_selector.setEnabled(False)
        
        self.y_selector_layout.addWidget(self.y_selector_label)
        self.y_selector_layout.addWidget(self.y_axis_selector)
        self.left_layout.addLayout(self.y_selector_layout)

        

        self.file_name_label = QLabel("自定義圖片檔名：")
        self.left_layout.addWidget(self.file_name_label)

        self.file_name_input = QLineEdit()
        self.file_name_input.textChanged.connect(self.validate_inputs)
        self.left_layout.addWidget(self.file_name_input)
        
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red; font-size: 15px;")
        self.left_layout.addWidget(self.error_label)

        self.plot_button = QPushButton("繪製圖表")
        self.plot_button.clicked.connect(self.plot_data)
        self.plot_button.setEnabled(False)
        self.left_layout.addWidget(self.plot_button)

        self.file_list_widget = QListWidget()
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.file_list_widget.setSizePolicy(size_policy)
        self.main_layout.addWidget(self.file_list_widget)
        

        self.setLayout(self.main_layout)

    def validate_inputs(self):
        file_loaded, fileMsg = self.check_file_loaded()
        file_name_valid,fileNameMsg = self.check_file_name()
        self.plot_button.setEnabled(file_loaded and file_name_valid)
        self.msg_show(fileMsg,fileNameMsg)
        
    def msg_show(self,fileMsg, fileNameMsg):
        if len(fileMsg) == 0:
            self.error_label.setText(fileNameMsg)
        else:
            self.error_label.setText(fileMsg)
    
    def check_file_loaded(self):
        try:
            if not self.csv_files:
                return False,'請先選擇CSV檔案'
            else:
                return True,''
        except: # workaround 程式啟動時的檢查
            return False,'請先選擇CSV檔案'
    
    def check_file_name(self):
        file_name = self.file_name_input.text().strip()
        if not file_name:
            return False,'檔案名稱不可為空'
        elif not self.is_valid_file_name(file_name):
            return False,'檔案名稱不合法'
        else:
            return True,''

    def is_valid_file_name(self, file_name):
        invalid_chars = r'[\\/:"*?<>|]'
        return not bool(re.search(invalid_chars, file_name))

