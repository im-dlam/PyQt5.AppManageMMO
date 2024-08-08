from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
import sys

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        button = QPushButton('Button with Pink Stripe', self)
        button.setStyleSheet("""
            QPushButton {
                background-color: #2D2E40;  /* Background color */
                color: #FFF;  /* Text color */
                border: none;  /* No border */
                padding: 5px;  /* Padding for the button */
                text-align: center;  /* Center the text */
            }
        """)

        # Create a layout to overlay the stripe on the button
        button_layout = QVBoxLayout(button)
        button_layout.setContentsMargins(0, 0, 250, 0)
        button_layout.setAlignment(Qt.AlignCenter)
        
        # Create the pink stripe
        pink_stripe = QLabel()
        pink_stripe.setFixedHeight(10)
        pink_stripe.setStyleSheet("background-color: #FF69B4;border-radius:10px")

        button_layout.addWidget(pink_stripe)

        vbox.addWidget(button)
        self.setLayout(vbox)

        self.setWindowTitle('Custom QPushButton')
        self.setGeometry(300, 300, 300, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
