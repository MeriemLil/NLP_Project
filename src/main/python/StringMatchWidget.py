import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from sqlalchemy import create_engine 


class StringMatchWidget(QWidget): 
    def __init__(self): 
        super(StringMatchWidget, self).__init__()
        self.initUI()


    def initUI(self):

        stringMatchingAccuracy = 0.33575
        empathAccuracy = 0.14305
        empathExactCategoryAccuracy = 0.18285

        grid = QGridLayout()
        self.setLayout(grid)
        
        scroll = QScrollArea()
        layout = QVBoxLayout()
        table = QTableWidget()

        table.setColumnCount(2)
        # set row count of table
        table.setRowCount(4)
        table.setItem(0,0,QTableWidgetItem('Type'))
        table.setItem(0,1,QTableWidgetItem('Accuracy'))

        table.setItem(1,0,QTableWidgetItem('String Matching'))
        table.setItem(1,1,QTableWidgetItem(str(stringMatchingAccuracy)))

        table.setItem(2,0,QTableWidgetItem('Empath client prediction'))
        table.setItem(2,1,QTableWidgetItem(str(empathAccuracy)))

        table.setItem(3,0,QTableWidgetItem('Empath using exact categories'))
        table.setItem(3,1,QTableWidgetItem(str(empathExactCategoryAccuracy)))
        
        scroll.setWidget(table)
        grid.addWidget(table) 
        self.show()


        
   