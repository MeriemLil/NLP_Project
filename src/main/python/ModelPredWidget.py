import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import requests

class ModelPredWidget(QWidget): 
    def __init__(self): 
        super(ModelPredWidget, self).__init__()
        self.initUI()

  

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        
        self.label = QLabel("Input one or more test sentences, separated by a semicolon (;)\nA CNN model will predict the emotion state.")
        grid.addWidget(self.label, 0, 0)
        
        self.textbox = QLineEdit(self)
        self.textbox.resize(280,40)
        grid.addWidget(self.textbox, 1, 0)
        
        button = QPushButton('Show text', self)
        button.clicked.connect(self.populate)
        grid.addWidget(button, 1, 1)
        
        self.textlabel = QLabel("Sentences provided:")
        grid.addWidget(self.textlabel, 2, 0)
        
        self.sentences = QLabel("")
        grid.addWidget(self.sentences, 3, 0)
        
        self.predlabel = QLabel("Model predictions:")
        self.prediction = QLabel("")
        
        grid.addWidget(self.predlabel, 2, 1)
        grid.addWidget(self.prediction, 3, 1)
     
    def populate(self):

        text = self.textbox.text()
        pred = self.predict(text)
        text = text.split(';')
        text = '\n'.join(text)        
        self.sentences.setText(text)
        self.prediction.setText(pred)
        
    def predict(self, text):
        url = 'http://35.192.56.167/get_preds?msg='
        pred = requests.get(url+text).json()['response']
        return pred.replace(';', '\n')
        