from PyQt6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout

def say_hello():
    print("Hello, Wayne!")

app = QApplication([])
window = QWidget()
window.setWindowTitle("Advanced Optimizer Pro")

layout = QVBoxLayout()
button = QPushButton("Start Optimization")
button.clicked.connect(say_hello) # PyQt uses "Signals and Slots" for logic

layout.addWidget(button)
window.setLayout(layout)

window.show()
app.exec()