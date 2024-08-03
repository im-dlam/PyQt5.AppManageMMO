import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QLabel, QWidget
from PyQt5.QtGui import QFont, QColor, QPainter
from PyQt5.QtCore import Qt, pyqtSignal

class Overlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_StyledBackground, True)
        # self.setStyleSheet("background-color: rgba(0, 0, 0, 128);")
        self.setGeometry(parent.rect())
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 128))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 600, 400)

        self.button = QPushButton("Open Dialog", self)
        self.button.setGeometry(200, 150, 200, 50)
        self.button.clicked.connect(self.open_dialog)
    
    def open_dialog(self):
        self.overlay = Overlay(self)
        self.overlay.show()
        
        self.dialog = CustomDialog(self)
        self.dialog.finished.connect(self.remove_overlay)
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()
    
    def remove_overlay(self):
        self.overlay.hide()

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Custom Dialog")
        self.setGeometry(150, 150, 300, 200)
        
        layout = QVBoxLayout()
        
        label = QLabel("This is a custom dialog", self)
        label.setFont(QFont("Arial", 16))
        layout.addWidget(label)
        
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
