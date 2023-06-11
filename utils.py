import pandas as pd
from PyQt5.QtWidgets import QLabel,QPushButton
def read_csv(file_name):
    try:
        data = pd.read_csv(file_name)
        return data, None
    except Exception as e:
        return None, str(e)

def generate_file_name_label(file_name):
    file_label = QLabel(file_name)
    file_label.setStyleSheet("border: none;")
    return file_label

# 加入用來叫出彈跳視窗的按鈕
def generate_item_button(item_name,apply_function):
    edit_button = QPushButton(item_name)
    edit_button.setFixedSize(60, 30)
    edit_button.setStyleSheet("border: 1px solid black;")
    edit_button.clicked.connect(apply_function)
    return edit_button