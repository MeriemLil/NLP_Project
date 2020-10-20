import pandas as pd
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from sqlalchemy import create_engine

class BowDetailedTable(QWidget): 
    def __init__(self): 
        super(BowDetailedTable, self).__init__()
        self.engine = create_engine('sqlite:///data/project.db', echo=False)
        self.df = pd.read_sql('SELECT * FROM bestModels', con=self.engine, index_col='index')
        self.df.set_index('name', inplace=True, drop=True)
        print(self.df.columns)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        dropdown = QComboBox()
        dropdown.addItems(['Model Statistics','Confusion Matrices', 'CNN Hyperparameters'])
        grid.addWidget(dropdown, 0, 0)
        
        btn1 = QPushButton('Show table', self)
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(lambda: self.populate(arg=dropdown.currentText()))
        grid.addWidget(btn1, 0, 1)
    
        scroll = QScrollArea()
        self.table = QTableWidget()
        
        scroll.setWidget(self.table)
        scroll.setAlignment(Qt.AlignHCenter)
        
        grid.addWidget(scroll)
        self.show()
        
     
    def populate(self, arg):
        if arg == 'Model Statistics':
            dataframe = self.df.iloc[:,:6].round(3)
            self.table.setFixedWidth(737)
        if arg == 'CNN Hyperparameters':
            dataframe = self.df.iloc[-2:,[0]+[i for i in range(6,12)]]
            dataframe.acc = dataframe.acc.round(3)
            self.table.setFixedWidth(787) 
        if arg == 'Confusion Matrices':
            dataframe = self.df.iloc[:,12::4]
            dataframe2 = self.df.iloc[:,13::4]
            dataframe3 = self.df.iloc[:,14::4]
            dataframe4 = self.df.iloc[:,15::4]
            self.table.setFixedWidth(737)
            self.table.setFixedHeight(350)
            indx = dataframe.index.to_list()
            indx = np.repeat(indx, 2)
            self.table.setColumnCount(len(dataframe.columns))
            self.table.setRowCount(2*len(dataframe.index))
            self.table.setHorizontalHeaderLabels(dataframe.columns.str[:-3])
            self.table.setVerticalHeaderLabels(indx)
            for i in range(len(dataframe.index)):
                for j in range(len(dataframe.columns)):
                    str_upper = str(dataframe4.iloc[i,j]) + '   |   ' + str(dataframe2.iloc[i,j])
                    str_lower = str(dataframe3.iloc[i,j]) + '   |   ' + str(dataframe.iloc[i,j])
                    self.table.setItem(i*2,j,QTableWidgetItem(str_upper))
                    self.table.setItem(i*2+1,j,QTableWidgetItem(str_lower))
        if arg != 'Confusion Matrices':
            self.table.setColumnCount(len(dataframe.columns))
            self.table.setRowCount(len(dataframe.index))
            self.table.setHorizontalHeaderLabels(dataframe.columns)
            self.table.setVerticalHeaderLabels(dataframe.index)
            for i in range(len(dataframe.index)):
                for j in range(len(dataframe.columns)):
                    self.table.setItem(i,j,QTableWidgetItem(str(dataframe.iloc[i,j])))

			