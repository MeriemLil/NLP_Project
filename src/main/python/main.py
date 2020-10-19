import sys
from PyQt5.QtWidgets import *
from PlotWidget import PlotWidget



class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Create the maptlotlib FigureCanvas object, 
        # which defines a single set of axes as self.axes.
        sc = PlotWidget()
        self.setCentralWidget(sc)

        self.show()

app = QApplication(sys.argv)
w = MainWindow()
app.exec_()  