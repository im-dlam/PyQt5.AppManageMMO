from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QPainter

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setFixedHeight(30)
        self.setStyleSheet("background-color: black; color: white;")

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel("Custom Title Bar")
        self.title.setStyleSheet("color: white;")
        self.layout.addWidget(self.title)

        self.btnMinimize = QPushButton("-")
        self.btnMinimize.setFixedSize(30, 30)
        self.btnMinimize.clicked.connect(parent.showMinimized)
        self.layout.addWidget(self.btnMinimize)

        self.btnMaximize = QPushButton("[]")
        self.btnMaximize.setFixedSize(30, 30)
        self.btnMaximize.clicked.connect(self.toggleMaximize)
        self.layout.addWidget(self.btnMaximize)

        self.btnClose = QPushButton("X")
        self.btnClose.setFixedSize(30, 30)
        self.btnClose.clicked.connect(parent.close)
        self.layout.addWidget(self.btnClose)

        self.setLayout(self.layout)

    def toggleMaximize(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.window().move(self.window().pos() + delta)
        self.oldPos = event.globalPos()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white;")

        self.titleBar = CustomTitleBar(self)
        self.setMenuWidget(self.titleBar)

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)

        layout = QVBoxLayout(self.mainWidget)
        label = QLabel("Main content area")
        layout.addWidget(label)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(self.rect())

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
