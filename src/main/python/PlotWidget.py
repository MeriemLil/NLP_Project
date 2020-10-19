import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class PlotWidget(QWidget):
    def __init__(self):
        super(PlotWidget, self).__init__()
        self.df = pd.read_json('ml/results/results.json')
        self.df['max_features'] = self.df.max_features.fillna('Full  ').astype(str).str[:-2]
        self.initUI()

    def initUI(self):
        
        self.setGeometry(100, 60, 1000, 800) 
        self.setWindowTitle('Plots')
        self.center()
        self.setWindowTitle('S Plot')

        grid = QGridLayout()
        self.setLayout(grid)
        
        
        dropdown = QComboBox()
        dropdown.addItems(self.df.columns[:-1])
        grid.addWidget(dropdown, 1, 1)
        
        btn1 = QPushButton('Plot', self)
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(lambda: self.plot(estimator=np.mean,
                                col=dropdown.currentText()))
        grid.addWidget(btn1, 1, 0)
    

        self.figure = Figure(figsize=(10, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        grid.addWidget(self.canvas, 3, 0, 1, 2)

        self.show()

    def plot(self, estimator, col):
        sns.set_style("darkgrid")
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        a = self.df.groupby(col)['score'].aggregate(estimator).reset_index()
        a = a.sort_values('score', ascending=False)
        ax = sns.barplot(data = self.df, x=col, y='score', estimator=estimator,
                    order=a[col], hue=col, hue_order=a[col],
                    ci=None, capsize=.2, ax=ax, dodge=False)
        ax.set(xticklabels=[], xlabel='', ylim=(0,1), ylabel='')
        ax.set_title(col.capitalize())
        ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.2)
        self.figure.subplots_adjust(left=0.2, right=0.7, bottom=0.01, top=0.9)
        self.figure.suptitle('Comparison of dev set accuracies with different setups',
                     fontsize=16, x=4, y=0.95)
        self.canvas.draw_idle()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())