import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from sqlalchemy import create_engine

class HarvardInqDBWidget(QWidget): 
    def __init__(self): 
        super(HarvardInqDBWidget, self).__init__()
        self.engine = create_engine('sqlite:///data/project.db', echo=False)
        self.initUI()

  

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        dropdown = QComboBox()
        dropdown.addItems(self.engine.table_names())
        grid.addWidget(dropdown, 0, 0)
        
        btn1 = QPushButton('Show database, or sample from database', self)
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(lambda: self.populate(dropdown.currentText()))
        grid.addWidget(btn1, 0, 1)

        self.table = QTableWidget()
        self.table.setFixedWidth(749)
        self.table.setFixedHeight(656)
        grid.addWidget(self.table) 
        self.show()
        
     
    def populate(self, table_name):
        self.df = pd.read_sql('SELECT * FROM ' + table_name + ' LIMIT 1000', con=self.engine)
        dataframe = self.df
        self.table.setColumnCount(len(dataframe.columns))
        self.table.setRowCount(len(dataframe.index))
        self.table.setHorizontalHeaderLabels(dataframe.columns)
        self.table.verticalHeader().hide()
        for i in range(len(dataframe.index)):
            for j in range(len(dataframe.columns)):
                self.table.setItem(i,j,QTableWidgetItem(str(dataframe.iloc[i, j])))

        