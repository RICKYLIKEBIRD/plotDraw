from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QPushButton, QHBoxLayout, QComboBox
from PyQt5 import QtCore

class AxisSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window)

        self.x_axis_selector = QComboBox()
        self.y_axis_selector = QComboBox()

        self.setWindowTitle("選擇 X 軸和 Y 軸")
    
        vbox = QVBoxLayout()
        form_layout = QFormLayout()
        form_layout.addRow("X 軸:", self.x_axis_selector)
        form_layout.addRow("Y 軸:", self.y_axis_selector)
        vbox.addLayout(form_layout)
    
        hbox = QHBoxLayout()
        self.save_button = QPushButton("儲存")
        self.save_button.clicked.connect(self.accept)
        hbox.addWidget(self.save_button)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        hbox.addWidget(self.cancel_button)
        vbox.addLayout(hbox)
    
        self.setLayout(vbox)
