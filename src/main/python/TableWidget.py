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
        
        l1 = QLabel()
        l2 = QLabel()
        l1.setText("This widget shows accuracies of bag-of-words models and pre processing strategies we used in the project.")
        l2.setText("Select a strategy from below and click show table to view the accuracy table.")
        
        grid.addWidget(l1)
        grid.addWidget(l2)

        dropdown = QComboBox()
        dropdown.addItems(self.df.columns[:-1])
        grid.addWidget(dropdown, 2, 0)

        dropdown2 = QComboBox()
        dropdown2.addItems(['max','mean'])
        grid.addWidget(dropdown2, 2, 1)
        
        btn1 = QPushButton('Show table', self)
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(lambda: self.populate(col=dropdown.currentText(),
                                                   method=dropdown2.currentText()))
        grid.addWidget(btn1, 2, 2)
    
        scroll = QScrollArea()
        self.table = QTableWidget()
        self.table.setFixedHeight(600)
        self.table.setFixedWidth(1024)
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