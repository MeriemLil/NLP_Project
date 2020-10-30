import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
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
        
        dropdown2 = QComboBox()
        dropdown2.addItems(['max','mean'])
        grid.addWidget(dropdown2, 0, 1)
        
        btn1 = QPushButton('Show table', self)
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(lambda: self.populate(col=dropdown.currentText(),
                                                   method=dropdown2.currentText()))
        grid.addWidget(btn1, 0, 2)
    
        scroll = QScrollArea()
        self.table = QTableWidget()
        self.table.setFixedHeight(300)
        self.table.setFixedWidth(202)
        scroll.setWidget(self.table)
        scroll.setAlignment(Qt.AlignHCenter)
        
        grid.addWidget(scroll)
        self.show()
        
     
    def populate(self, col, method):
        dataframe = self.df.groupby(col)['score'].agg(method) * 100
        dataframe = dataframe.sort_values(ascending=False).round(2)
        self.table.setColumnCount(2)
        self.table.setRowCount(len(dataframe.index))
        self.table.setHorizontalHeaderLabels([col, 'Accuracy'])
        self.table.verticalHeader().hide()
        for i in range(len(dataframe.index)):
            self.table.setItem(i,0,QTableWidgetItem(str(dataframe.index[i])))
            self.table.setItem(i,1,QTableWidgetItem(str(dataframe.iloc[i])+'%'))