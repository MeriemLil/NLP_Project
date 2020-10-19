import sys
from PyQt5.QtWidgets import *
from changeVisibility import changeVisibility


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(200, 200, 1024, 768)
        self.main_widget = QWidget(self)
        
        self.main_layout = QVBoxLayout(self.main_widget)
        
        
        self.main_layout.addWidget(changeVisibility())    
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.show()




app = QApplication(sys.argv)
app.setStyle('Fusion')
w = MainWindow()
app.exec_()  