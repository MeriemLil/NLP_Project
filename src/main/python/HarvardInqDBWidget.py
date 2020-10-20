import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from sqlalchemy import create_engine
# from patternMatch.categorySetup import * 

class HarvardInqDBWidget(QWidget): 
    def __init__(self): 
        super(HarvardInqDBWidget, self).__init__()
        self.engine = create_engine('sqlite:///data/project.db', echo=False)
        self.df = pd.read_sql('SELECT * FROM harvardWords', con=self.engine)
        self.initUI()

  

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        btn1 = QPushButton('Show database', self)
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(lambda: self.populate())
        grid.addWidget(btn1, 0, 1)
    
        scroll = QScrollArea()
        self.table = QTableWidget()
        self.table.setFixedHeight(600)
        self.table.setFixedWidth(316)
        scroll.setWidget(self.table)
        scroll.setAlignment(Qt.AlignHCenter)
        grid.addWidget(scroll) 
        self.show()
        
     
    def populate(self):
        self.df['entry'] = self.df.entry.astype(str)
        self.df['emotion_type'] = self.df.emotion_type.astype(str)
        dataframe = self.df
        self.table.setColumnCount(3)
        self.table.setRowCount(len(dataframe.index))
        self.table.setHorizontalHeaderLabels(['Id', 'Entry', 'Emotion Type'])
        self.table.verticalHeader().hide()
        for i in range(len(dataframe.index)):
            self.table.setItem(i,0,QTableWidgetItem(str(dataframe.index[i])))
            self.table.setItem(i,1,QTableWidgetItem(str(dataframe.iloc[i].entry)))
            self.table.setItem(i,2,QTableWidgetItem(str(dataframe.iloc[i].emotion_type)))

        