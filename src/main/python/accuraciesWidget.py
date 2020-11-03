from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
def on_clicked(val):
    alert = QMessageBox()
    alert.setText(val)
    alert.exec_()

class accuraciesWidget(QWidget):
    def __init__(self):
        super(accuraciesWidget, self).__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        methods = ['Empath client', 'Empath with exact categories',
        'Harvard String Matching','Semantic Similarity, one synset',
        'Semantic Similarity, all synsets']
        accuracies = ['0.16045', '0.18285', '0.33575','0.2685', '0.23955']
    
        l1 = QLabel()
        l1.setText("This widget shows accurecies of the five methods we used in the project in table format.")
        
        grid.addWidget(l1)
        scroll = QScrollArea()
        self.table = QTableWidget()
        self.table.setFixedWidth(739)
        
        self.table.setColumnCount(len(methods))
        self.table.setRowCount(1)
        self.table.setHorizontalHeaderLabels(methods)
        self.table.verticalHeader().hide()
        for i in range(len(accuracies)):
            self.table.setItem(0,i,QTableWidgetItem(accuracies[i]))
        
        scroll.setWidget(self.table)
        scroll.setAlignment(Qt.AlignHCenter)
        self.table.resizeColumnsToContents()
        grid.addWidget(scroll)
        self.show()
        
        