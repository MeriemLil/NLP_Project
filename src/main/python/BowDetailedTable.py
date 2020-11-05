import pandas as pd
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from DatabaseConn import database_connect

class BowDetailedTable(QWidget): 
    def __init__(self): 
        super(BowDetailedTable, self).__init__()
        self.engine = database_connect()
        self.df = pd.read_sql('SELECT * FROM bestModels', con=self.engine)
        self.df.set_index('name', inplace=True, drop=True)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        l1 = QLabel()
        l2 = QLabel()
        l1.setText("This widget shows machine learning models results.")
        l2.setText("Select an option from below and click show to view the results.")
        
        grid.addWidget(l1)
        grid.addWidget(l2)

        dropdown = QComboBox()
        dropdown.addItems(['Model Statistics','Confusion Matrices', 'CNN Hyperparameters'])
        grid.addWidget(dropdown, 2, 0)
        
        btn1 = QPushButton('Show table', self)
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(lambda: self.populate(arg=dropdown.currentText()))
        grid.addWidget(btn1, 2, 1)
    
        scroll = QScrollArea()
        self.table = QTableWidget()
        self.table.setFixedWidth(1024)
        self.table.setFixedHeight(768)
        
        scroll.setWidget(self.table)
        scroll.setAlignment(Qt.AlignHCenter)
        
        grid.addWidget(scroll)
        self.show()
        
     
    def populate(self, arg):
        if arg == 'Model Statistics':
            dataframe = self.df.iloc[:,:6].round(3)
        if arg == 'CNN Hyperparameters':
            dataframe = self.df.iloc[-2:,[0]+[i for i in range(6,12)]]
            dataframe.acc = dataframe.acc.round(3)
        if arg == 'Confusion Matrices':
            dataframe = self.df.loc[:,self.df.columns.str.contains('_tn')]
            dataframe2 = self.df.loc[:,self.df.columns.str.contains('_fp')]
            dataframe3 = self.df.loc[:,self.df.columns.str.contains('_fn')]
            dataframe4 = self.df.loc[:,self.df.columns.str.contains('_tp')]
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

			