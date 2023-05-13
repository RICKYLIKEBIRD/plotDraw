import sys
from PyQt5.QtWidgets import QApplication
from csv_reader_app import CsvReaderApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CsvReaderApp()
    window.show()
    sys.exit(app.exec_())
