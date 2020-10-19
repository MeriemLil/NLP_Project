from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QMessageBox

def on_button_clicked(val):
    alert = QMessageBox()
    alert.setText(val)
    alert.exec_()

app = QApplication([])
app.setStyle('Fusion')

window = QWidget()
window.setWindowTitle('Emotion Analysis')
window.setGeometry(50, 50, 400, 100)

layout = QVBoxLayout()
label = QLabel('Find Accuracy')
layout.addWidget(label)

button1 = QPushButton('String Matching')
button2 = QPushButton('Empath Client')
button3 = QPushButton('Semantic Similarity')

button1.clicked.connect(lambda: on_button_clicked('0.5'))
button2.clicked.connect(lambda: on_button_clicked('0.3'))
button3.clicked.connect(lambda: on_button_clicked('0.2'))

layout.addWidget(button1)
layout.addWidget(button2)
layout.addWidget(button3)

window.setLayout(layout)

window.show()

app.exec_()