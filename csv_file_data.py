# 在 csvFileData.py 文件中
class CSVFileData:
    def __init__(self, file_base_name, data, file_item, file_widget, x_axis_selector, y_axis_selector):
        self.file_base_name = file_base_name
        self.data = data
        self.file_item = file_item
        self.file_widget = file_widget
        self.x_axis_selector = x_axis_selector
        self.y_axis_selector = y_axis_selector
        self.x_selector_current_index = None
        self.y_selector_current_index = None
        self.x_value = data.columns[0]
        self.y_value = data.columns[1]
        
    def get_x_selector_current_index(self):
        return self.x_selector_current_index or 0
    
    def get_y_selector_current_index(self):
        return self.y_selector_current_index or 0


