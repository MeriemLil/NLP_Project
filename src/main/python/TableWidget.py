import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from sqlalchemy import create_engine


class TableWidget(QWidget): 
    def __init__(self): 
        super(TableWidget, self).__init__()
        self.engine = create_engine('sqlite:///data/project.db', echo=False)
        self.df = pd.read_sql('SELECT * FROM bowModels', con=self.engine)
        self.df['max_features'] = self.df.max_features.fillna('Full  ').astype(str).str[:-2]
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        dropdown = QComboBox()
        dropdown.addItems(self.df.columns[:-1])
        grid.addWidget(dropdown, 0, 0)
        
        btn1 = QPushButton('Show table', self)
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(lambda: self.populate(col=dropdown.currentText(), table=table))
        grid.addWidget(btn1, 0, 1)
    
        scroll = QScrollArea()
        layout = QVBoxLayout()
        table = QTableWidget()
        scroll.setWidget(table)
        grid.addWidget(table) 
        self.show()
        
     
    def populate(self, col, table):
        dataframe = self.df.groupby(col)['score'].agg('mean') * 100
        dataframe = dataframe.round(2)
        table.setColumnCount(2)
        table.setRowCount(len(dataframe.index)+1)
        table.setItem(0,0,QTableWidgetItem(col))
        table.setItem(0,1,QTableWidgetItem('score'))
        for i in range(1, len(dataframe.index)+1):
            table.setItem(i,0,QTableWidgetItem(str(dataframe.index[i-1])))
            table.setItem(i,1,QTableWidgetItem(str(dataframe.iloc[i-1])+'%'))
        