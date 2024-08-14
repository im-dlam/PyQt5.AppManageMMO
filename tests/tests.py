import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame
from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve

class ToggleSwitch(QPushButton):
    def __init__(self, parent=None):
        super(ToggleSwitch, self).__init__(parent)
        self.setCheckable(True)
        self.setMinimumWidth(60)
        self.setMinimumHeight(30)
        self.setStyleSheet(self._get_stylesheet())

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.clicked.connect(self.start_animation)

    def _get_stylesheet(self):
        return """
        ToggleSwitch {
            background-color: #555;
            border-radius: 15px;
            border: 1px solid #ccc;
        }
        ToggleSwitch:checked {
            background-color: #007BFF;
        }
        ToggleSwitch:checked::before {
            content: '';
            position: absolute;
            top: 3px;
            left: 33px;
            width: 24px;
            height: 24px;
            border-radius: 12px;
            background-color: white;
        }
        ToggleSwitch::before {
            content: '';
            position: absolute;
            top: 3px;
            left: 3px;
            width: 24px;
            height: 24px;
            border-radius: 12px;
            background-color: white;
            transition: left 0.2s ease;
        }
        """

    def start_animation(self):
        if self.isChecked():
            self.animation.setStartValue(QRect(3, 3, 24, 24))
            self.animation.setEndValue(QRect(33, 3, 24, 24))
        else:
            self.animation.setStartValue(QRect(33, 3, 24, 24))
            self.animation.setEndValue(QRect(3, 3, 24, 24))
        self.animation.start()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Toggle Switch Example")
        self.setGeometry(100, 100, 200, 100)

        self.frame = QFrame(self)
        self.frame.setGeometry(20, 20, 160, 60)
        self.frame.setStyleSheet("background-color: #333; border-radius: 15px;")

        self.toggle = ToggleSwitch(self.frame)
        self.toggle.setGeometry(50, 15, 60, 30)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
