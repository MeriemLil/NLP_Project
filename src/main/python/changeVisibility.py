from PlotWidget import PlotWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class changeVisibility(QWidget):    
    def __init__(self, parent=None):        
        super(changeVisibility, self).__init__(parent)
        self.pw = PlotWidget()

        button_bow = QPushButton('Bag of Words model plots')
        button_bow.clicked.connect(lambda: self.pw.show())
        
        
        button_home = QPushButton('Home')
        button_home.clicked.connect(lambda: self.pw.hide())
        
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(button_bow)
        self.verticalLayout.addWidget(button_home)
        self.verticalLayout.setAlignment(Qt.AlignTop)
        self.verticalLayout.addWidget(self.pw)
        self.pw.hide()