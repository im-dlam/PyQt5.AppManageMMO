import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
from PyQt5.QtGui import QMovie, QIcon
from PyQt5.QtCore import QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GIF Icon Example")
        self.setGeometry(100, 100, 300, 200)

        self.button = QPushButton("Button with GIF Icon", self)
        self.button.setGeometry(50, 50, 200, 100)

        # Load the GIF file
        self.movie = QMovie(r"D:\UI Python\GUI_PyQt5_My_App\icons\gif\icons8-todo-list.gif")
        self.movie.start()

        # Create an icon from the movie and set it to the button
        self.update_icon()
        self.movie.frameChanged.connect(self.update_icon)

    def update_icon(self):
        frame = self.movie.currentPixmap()
        icon = QIcon(frame)
        self.button.setIcon(icon)
        self.button.setIconSize(QSize(64, 64))  # Adjust the size as needed

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
   
