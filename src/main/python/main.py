from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
from PyQt5.QtWidgets import *
from changeVisibility import changeVisibility


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.main_widget = QWidget(self)
        self.setGeometry(200, 200, 1024, 768)
        self.setWindowTitle('NLP Project GUI') 
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.addWidget(changeVisibility())    
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.show()

 
if __name__ == '__main__':
    appctxt = ApplicationContext()
    appctxt.app.setStyle('Fusion')
    w = MainWindow()
    w.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)