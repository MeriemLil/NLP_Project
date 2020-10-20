import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from sqlalchemy import create_engine
from patternMatch.categorySetup import * 


class HarvardInqDBWidget(QWidget): 
    def __init__(self): 
        super(HarvardInqDBWidget, self).__init__()
        self.engine = create_engine('sqlite:///data/project.db', echo=False)
        # if not engine.has_table('harvardWords'):
        #     self.df = assign_category(category_list, harvardInquirer)
        #     print('Database created successfully')
        # else:
        #     print("Database creation Done")
        #     self.df = pd.read_sql('SELECT * FROM bowModels', con=self.engine)
        self.df = pd.read_sql('SELECT * FROM harvardWords', con=self.engine)
        self.initUI()

  

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        btn1 = QPushButton('Show database', self)
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(lambda: self.populate(col='id', table=table))
        grid.addWidget(btn1, 0, 1)
    
        scroll = QScrollArea()
        layout = QVBoxLayout()
        table = QTableWidget()
        scroll.setWidget(table)
        grid.addWidget(table) 
        self.show()
        
     
    def populate(self, col, table):
        self.df['entry'] = self.df.entry.astype(str)
        self.df['emotion_type'] = self.df.emotion_type.astype(str)
        dataframe = self.df
        table.setColumnCount(3)
        table.setRowCount(len(dataframe.index)+1)
        table.setItem(0,0,QTableWidgetItem(col))
        table.setItem(0,1,QTableWidgetItem('entry'))
        table.setItem(0,2, QTableWidgetItem('emotion_type'))

        for i in range(1, len(dataframe.index)+1):
            table.setItem(i,0,QTableWidgetItem(str(dataframe.index[i-1])))
            table.setItem(i,1,QTableWidgetItem(str(dataframe.iloc[i-1].entry)))
            table.setItem(i,2,QTableWidgetItem(str(dataframe.iloc[i-1].emotion_type)))

        