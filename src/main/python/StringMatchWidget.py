import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from sqlalchemy import create_engine 


class StringMatchWidget(QWidget): 
    def __init__(self): 
        super(StringMatchWidget, self).__init__()
        # self.engine = create_engine('sqlite:///data/project.db', echo=False)
        # self.df = pd.read_sql('SELECT * FROM harvardWords', con=self.engine)
        self.initUI()


    def initUI(self):
        self.layout = QVBoxLayout()
        self.label = QLabel("String matching Accuracy: "+'50')
        self.layout.addWidget(self.label)

        self.setWindowTitle("String Matching Accuracy")
        self.setLayout(self.layout)
        self.show()
      

        
   