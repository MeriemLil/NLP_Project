from PyQt5.QtWidgets import *

def on_clicked(val):
    alert = QMessageBox()
    alert.setText(val)
    alert.exec_()

class accuraciesWidget(QWidget):
    def __init__(self):
        super(accuraciesWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        button1 = QPushButton('Empath Client 1')
        button1.clicked.connect(lambda: on_clicked('Accuracy of Empath client prediction: 0.16045'))
        button2 = QPushButton('Empath Client 2')
        button2.clicked.connect(lambda: on_clicked('Accuracy of Empath client prediction with exact categories: 0.18285'))
        button3 = QPushButton('String Matching')
        button3.clicked.connect(lambda: on_clicked('Accuracy of String Matching: 0.33575'))
        button4 = QPushButton('Semantic Similarity 1')
        button4.clicked.connect(lambda: on_clicked('Accuracy of Semantic Similarity, 1 category synset: 0.2685'))
        button5 = QPushButton('Semantic Similarity 2')
        button5.clicked.connect(lambda: on_clicked('Accuracy of Semantic Similarity, all category synsets: 0.23955'))

        self.layout.addWidget(button1)
        self.layout.addWidget(button2)
        self.layout.addWidget(button3)
        self.layout.addWidget(button4)
        self.layout.addWidget(button5)

        self.setWindowTitle("Accuracies")
        self.setLayout(self.layout)
        self.show()

