from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QListWidget, QSizePolicy, QFormLayout,QDialog
import re

class CsvReaderGui:
    def setup_gui(self):
        self.setWindowTitle("CSV讀取器")
        self.setGeometry(100, 100, 600, 300)

        self.main_layout = QHBoxLayout()

        self.left_layout = QVBoxLayout()

        self.open_button = QPushButton("打開CSV檔案")
        self.open_button.clicked.connect(self.open_csv)
        self.left_layout.addWidget(self.open_button)

        self.label = QLabel("選擇X軸和Y軸的欄位")
        self.left_layout.addWidget(self.label)

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

        self.main_layout.addLayout(self.left_layout)

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

