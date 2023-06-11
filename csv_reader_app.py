import os
from PyQt5.QtWidgets import QWidget, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidgetItem, QComboBox,QDialog,QFormLayout
from csv_reader_gui import CsvReaderGui
from axis_selection_dialog import AxisSelectionDialog
import utils
import matplotlib.pyplot as plt
from csv_file_data import CSVFileData


class CsvReaderApp(QWidget, CsvReaderGui):
    def __init__(self):
        super().__init__()

        self.setup_gui()
        self.csv_files = {}
        self.main_attr_status = False
        self.base_function_button_css = "font-weight: bold; border: 1px solid black; border-radius: 30px;"

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
                
    def get_function_button_style(self):
        return self.base_function_button_css + ("background-color: #82d985;" if self.main_attr_status else "background-color: #ed7288;")
            
    def test(self):
        self.enable_button.setText("啟用" if self.main_attr_status else "禁用")
        self.enable_button.setStyleSheet(self.get_function_button_style())
        self.main_attr_status = not self.main_attr_status
        self.x_axis_selector.setEnabled (self.main_attr_status)
        self.y_axis_selector.setEnabled (self.main_attr_status)
                
        
    def save_axis_selection(self, file_base_name,x_selector,y_selector):
        file_data = self.csv_files[file_base_name]
        file_data.x_selector = x_selector
        file_data.y_selector = y_selector
        file_data.x_selector_current_index = x_selector.currentIndex()
        file_data.y_selector_current_index = y_selector.currentIndex()
        
                
    def show_axis_select_dialog(self, file_base_name):
        file_data = self.csv_files[file_base_name]
        data = file_data.data

        x_selector_current_index = file_data.get_x_selector_current_index()
        y_selector_current_index = file_data.get_y_selector_current_index()

        dialog = AxisSelectionDialog(self)
        for col in data.columns:
            dialog.x_axis_selector.addItem(col)
            dialog.y_axis_selector.addItem(col)

        dialog.x_axis_selector.setCurrentIndex(x_selector_current_index)
        dialog.y_axis_selector.setCurrentIndex(y_selector_current_index)


        dialog.save_button.clicked.connect(lambda: self.save_axis_selection(file_base_name,dialog.x_axis_selector,dialog.y_axis_selector))

        dialog.exec_()

    def get_new_x_and_y_selector(self,columns):
        x_axis_selector = QComboBox()
        y_axis_selector = QComboBox()
        for col in columns:
            x_axis_selector.addItem(col)
            y_axis_selector.addItem(col)
        return x_axis_selector,y_axis_selector 

            
    def add_csv_file(self, file_name, data):
        file_base_name = os.path.basename(file_name)
        if file_base_name not in self.csv_files:
            
            # 在此處添加新的 x 和 y 軸選擇器
            x_axis_selector , y_axis_selector = self.get_new_x_and_y_selector(data.columns)
            
            # 在此處添加檔案到清單中
            file_item = QListWidgetItem()
            file_widget = QWidget()
            file_widget.setStyleSheet("border: 1px solid black; padding: 5px; margin: 2px;")
            
            file_layout = QHBoxLayout()

            file_layout.addWidget(utils.generate_file_name_label(file_base_name))
            file_layout.addStretch(1)
            file_layout.addWidget(utils.generate_item_button("編輯",lambda: self.show_axis_select_dialog(file_base_name)))
            file_layout.addWidget(utils.generate_item_button("移除",lambda: self.remove_csv_file(file_base_name, file_item)))
            file_layout.addStretch(1)

        
            file_widget.setLayout(file_layout)
            file_item.setSizeHint(file_widget.sizeHint())
            
            file_data = CSVFileData(file_base_name, data, file_item, file_widget, x_axis_selector, y_axis_selector)

            self.csv_files[file_base_name] = file_data
            self.file_list_widget.addItem(file_item)
            self.file_list_widget.setItemWidget(file_item, file_widget)

    def remove_csv_file(self, file_base_name, file_item):
        del self.csv_files[file_base_name]
        self.file_list_widget.takeItem(self.file_list_widget.row(file_item)) 
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
