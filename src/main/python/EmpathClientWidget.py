import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from sqlalchemy import create_engine 


class EmpathClientWidget(QWidget): 
    def __init__(self): 
        super(EmpathClientWidget, self).__init__()
        self.initUI()


    def initUI(self):
        self.layout = QVBoxLayout()
        self.label = QLabel("Accuracy of Empath client prediction: "+'50')
        self.label1 = QLabel("Accuracy of Empath using exact categories: "+'50')

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.label1)

        self.setWindowTitle("String Matching Accuracy")
        self.setLayout(self.layout)
        self.show()
      

        
   