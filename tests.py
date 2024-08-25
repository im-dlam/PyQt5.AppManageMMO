from PyQt5.QtWidgets import QApplication, QCheckBox, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        checkbox = QCheckBox()
        checkbox.setChecked(True)
        checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border-radius: 3px;
                border: 2px solid #00C2A8;
                background-color: transparent;
            }
            QCheckBox::indicator:checked {
                image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAOCAMAAADYmsdrAAAAUVBMVEX///9PT1CJiomGhoZhYWGvr68TExMZGRmDg4NDQ0Pm5ubv7++VlZWwsLCvr6+ytrJuW1fJzc5lZWWkpKTb29vIyMgtLS1NTU3g4ODb29unpw2fAAAAlElEQVQI12PABwQ8zAsWUAQCI8FZP9QMwQKUMDXFCJpCHxQkxg+IiGZTgSDOHSIgMJBQk2CDmUSWgFjVQhkgR6IHYFZDFxcXEvob7xCUiE5oHCQAMaAcSiUQg8oDhBRiKNmAiTZmBFELKAgJCgBKoSCIlgiI4FAYiLAdRSYPBRiwok6iCgAZHKmgRCMQpgAAAABJRU5ErkJggg==);
            }
        """)

        layout.addWidget(checkbox)

        self.setLayout(layout)
        self.setWindowTitle("Custom Checkbox Example")
        self.setGeometry(100, 100, 200, 100)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
