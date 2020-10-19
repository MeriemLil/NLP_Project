import pandas as pd
from PyQt5.QtWidgets import QWidget,QScrollArea, QTableWidget, QVBoxLayout,QTableWidgetItem
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
        scroll = QScrollArea()
        layout = QVBoxLayout()
        table = QTableWidget()
        scroll.setWidget(table)
        layout.addWidget(table)
        self.setLayout(layout)    

        table.setColumnCount(len(self.df.columns))
        table.setRowCount(len(self.df.index))
        for i in range(len(self.df.index)):
            for j in range(len(self.df.columns)):
                table.setItem(i,j,QTableWidgetItem(str(self.df.iloc[i, j])))
        self.show()