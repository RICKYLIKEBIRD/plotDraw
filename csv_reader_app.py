import os
from PyQt5.QtWidgets import QWidget, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidgetItem, QComboBox,QDialog,QFormLayout
from csv_reader_gui import CsvReaderGui
from axis_selection_dialog import AxisSelectionDialog
import utils
import matplotlib.pyplot as plt


class CsvReaderApp(QWidget, CsvReaderGui):
    def __init__(self):
        super().__init__()

        self.setup_gui()
        self.csv_files = {}

    def open_csv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "選擇CSV檔案", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if file_name:
            data, error_msg = utils.read_csv(file_name)
            if error_msg:
                self.label.setText("讀取CSV檔案失敗: " + error_msg)
            else:
                self.label.setText("讀取CSV檔案成功")
                self.add_csv_file(file_name, data)
                self.plot_button.setEnabled(True)
                self.validate_inputs()
                self.show_axis_select_dialog(os.path.basename(file_name))
                
    def update_axis_selectors(self, file_base_name, x_value, y_value):
        file_data = self.csv_files[file_base_name]
        x_selector = file_data['x_selector']
        y_selector = file_data['y_selector']
        x_selector.setCurrentText(x_value)
        y_selector.setCurrentText(y_value)
        
    def save_axis_selection(self, file_base_name):
        file_data = self.csv_files[file_base_name]
        file_data['x_selector_current_index'] = file_data['x_selector'].currentIndex()
        file_data['y_selector_current_index'] = file_data['y_selector'].currentIndex()
        
                
                
    def show_axis_select_dialog(self, file_base_name):
        file_data = self.csv_files[file_base_name]
        data = file_data['data']

        x_selector_current_index = file_data.get('x_selector_current_index', 0)
        y_selector_current_index = file_data.get('y_selector_current_index', 0)

        dialog = AxisSelectionDialog(self)
        for col in data.columns:
            dialog.x_axis_selector.addItem(col)
            dialog.y_axis_selector.addItem(col)

        dialog.x_axis_selector.setCurrentIndex(x_selector_current_index)
        dialog.y_axis_selector.setCurrentIndex(y_selector_current_index)

        file_data['x_selector'] = dialog.x_axis_selector
        file_data['y_selector'] = dialog.y_axis_selector

        dialog.save_button.clicked.connect(lambda: self.save_axis_selection(file_base_name))

        dialog.exec_()

            
    def add_csv_file(self, file_name, data):
        file_base_name = os.path.basename(file_name)
        if file_base_name not in self.csv_files:
            
            # 在此處添加新的 x 和 y 軸選擇器
            x_axis_selector = QComboBox()
            y_axis_selector = QComboBox()
            for col in data.columns:
                x_axis_selector.addItem(col)
                y_axis_selector.addItem(col)
        
            
            # 在此處添加檔案到清單中
            file_item = QListWidgetItem()
            file_widget = QWidget()
            file_widget.setStyleSheet("border: 1px solid black; padding: 5px; margin: 2px;")
            file_layout = QHBoxLayout()

            file_label = QLabel(file_base_name)
            file_label.setStyleSheet("border: none;")
            file_layout.addWidget(file_label)

            # 加入用來叫出彈跳視窗的按鈕
            edit_button = QPushButton("編輯")
            edit_button.setFixedSize(60, 30)
            edit_button.setStyleSheet("border: 1px solid black;")
            edit_button.clicked.connect(lambda: self.show_axis_select_dialog(file_base_name))
            file_layout.addWidget(edit_button)

            file_layout.addStretch(1)

            remove_button = QPushButton("移除")
            remove_button.setFixedSize(60, 30)
            remove_button.setStyleSheet("border: 1px solid black;")
            remove_button.clicked.connect(lambda: self.remove_csv_file(file_base_name, file_item, remove_button))
            file_layout.addWidget(remove_button)

            file_widget.setLayout(file_layout)
            file_item.setSizeHint(file_widget.sizeHint())
            
            # 將 x 和 y 軸選擇器添加到 self.csv_files 字典中
            self.csv_files[file_base_name] = {
                'data': data,
                'item': file_item, 
                'widget': file_widget, 
                'button': remove_button,
                'x_selector': x_axis_selector,
                'y_selector': y_axis_selector,
                'x_value': data.columns[0],
                'y_value': data.columns[1]
            }

            self.file_list_widget.addItem(file_item)
            self.file_list_widget.setItemWidget(file_item, file_widget)

    def remove_csv_file(self, file_base_name, file_item, remove_button):
        file_data = self.csv_files[file_base_name]
        # x_selector = file_data['x_selector']
        # y_selector = file_data['y_selector']
        del self.csv_files[file_base_name]
        self.file_list_widget.takeItem(self.file_list_widget.row(file_item))
        # self.axis_selectors_layout.removeRow(x_selector)
        # self.axis_selectors_layout.removeRow(y_selector)
        # len(self.csv_files)
        
        self.validate_inputs() #卡控
    

    def plot_data(self):
        x_column = self.x_axis_selector.currentText()
        y_column = self.y_axis_selector.currentText()
        x_title = self.x_title_input.text() or x_column
        y_title = self.y_title_input.text() or y_column
        file_name = self.file_name_input.text() or f"{x_column}_vs_{y_column}"

        for file_base_name, file_data in self.csv_files.items():
            ax = file_data['data'].plot(x=x_column, y=y_column, kind='scatter')
            ax.set_xlabel(x_title)
            ax.set_ylabel(y_title)
            plt.savefig(os.path.join(os.path.dirname(file_base_name), f"{file_name}_{file_base_name}.png"))
