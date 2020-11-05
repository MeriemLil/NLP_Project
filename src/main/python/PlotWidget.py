import pandas as pd
import numpy as np

from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from sqlalchemy import create_engine


class PlotWidget(QWidget):
    def __init__(self):
        super(PlotWidget, self).__init__()
        self.engine = create_engine('sqlite:///data/project.db', echo=False)
        self.df = pd.read_sql('SELECT * FROM bowModels', con=self.engine)
        self.df['max_features'] = self.df.max_features.fillna('Full  ').astype(str).str[:-2]
        self.initUI()

    def initUI(self):
        
        self.center()
        grid = QGridLayout()
        self.setLayout(grid)
        
        l1 = QLabel()
        l2 = QLabel()
        l1.setText("This widget shows plots of bag-of-words models and preprocessing strategies we used in the project.")
        l2.setText("Select a strategy from below and click plot to view the graph.")
        
        grid.addWidget(l1)
        grid.addWidget(l2)

        dropdown = QComboBox()
        dropdown.addItems(self.df.columns[:-1])
        grid.addWidget(dropdown, 2, 0)
        
        dropdown_est = QComboBox()
        dropdown_est.addItems(['max','mean'])
        grid.addWidget(dropdown_est, 2, 1)

        btn1 = QPushButton('Plot', self)
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(lambda: self.plot(estimator=dropdown_est.currentText(),
                                col=dropdown.currentText()))
        grid.addWidget(btn1, 2, 2)
    

        self.figure = Figure(figsize=(10, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 3, 0, 1, 2)


    def plot(self, estimator, col):
        plt.style.use('seaborn-darkgrid')
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        a = self.df.groupby(col)['score'].aggregate(estimator).reset_index()
        a = a.sort_values('score', ascending=False)
        colors = ['lightcoral','lightblue','lightgreen','wheat','lightcyan','plum']
        
        ax.bar(x = a[col], height=a['score'], color=colors[:len(a)],
                    tick_label=['']*len(a))
        ax.set(xticklabels=[], xlabel='', ylim=(0,1), ylabel='')
        ax.set_title(col.capitalize(), fontsize='xx-large')
        ax.set_ylabel('Accuracy', fontsize='x-large')
        handles = [plt.Rectangle((0,0),1,1, color=colors[i]) for i in range(len(a))]
        ax.legend(handles, a[col], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.2)
        self.figure.subplots_adjust(left=0.1, right=0.7, bottom=0.1, top=0.9)
        self.figure.suptitle('Comparison of dev set accuracies with different setups',
                     fontsize=16, x=4, y=0.95)
        self.canvas.draw_idle()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())