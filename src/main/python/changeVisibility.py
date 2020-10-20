from PlotWidget import PlotWidget
from TableWidget import TableWidget
from HarvardInqDBWidget import HarvardInqDBWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class changeVisibility(QWidget):    
    def __init__(self, parent=None):        
        super(changeVisibility, self).__init__(parent)
        self.pw = PlotWidget()
        self.tw = TableWidget()
        self.harvardInqDB = HarvardInqDBWidget()


        button_home = QPushButton('Home')
        button_home.clicked.connect(lambda: return_to_main(self))
        
        button_bow = QPushButton('Bag of Words model plots')
        button_bow.clicked.connect(lambda: hide_all_but(self, self.pw))
        
        button_bow2 = QPushButton('Bag of Words model tables')
        button_bow2.clicked.connect(lambda: hide_all_but(self, self.tw))
        
        button_bow3 = QPushButton('Database created with harvard general inquirer')
        button_bow3.clicked.connect(lambda: hide_all_but(self, self.harvardInqDB))
        
        buttons = [button_bow, button_bow2, button_bow3]
        
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(button_home)
        self.layout.addWidget(button_bow3)
        self.layout.addWidget(button_bow)
        self.layout.addWidget(button_bow2)
        
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.pw)
        self.layout.addWidget(self.tw)
        self.layout.addWidget(self.harvardInqDB)
        self.pw.hide()
        self.tw.hide()
        self.harvardInqDB.hide()
        
        def hide_all_but(self, widget=None):
            """
            Helper function that hides all widgets except home and selected widget
            """
            for i in reversed(range(1, self.layout.count())):
                item = self.layout.itemAt(i)

                if isinstance(item, QWidgetItem):
                    item.widget().hide() 
                    # or
                    # item.widget().setParent(None)
            if widget is not None:
                widget.show()
                
        def return_to_main(self):
            """
            Helper function that renders all buttons and hides everything else.
            """
            for i in reversed(range(3, self.layout.count())):
                item = self.layout.itemAt(i)

                if isinstance(item, QWidgetItem):
                    item.widget().hide() 
            for i in reversed(range(1, 3)):
                item = self.layout.itemAt(i)
                if isinstance(item, QWidgetItem):
                    item.widget().show()
                        
          