import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

class SearchBar(QWidget):
    def __init__(self):
        super().__init__()
        
        # Create the main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create the search icon
        search_icon = QLabel(self)
        search_icon.setPixmap(QPixmap('search_icon.png'))  # Load your search icon here
        search_icon.setAlignment(Qt.AlignCenter)
        search_icon.setFixedSize(24, 24)  # Adjust size to fit your icon
        
        # Create the QLineEdit
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("What do you want to play?")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #FFFFFF;
                border-radius: 20px;
                padding-left: 35px;  # To make space for the icon
                padding-right: 35px;  # For padding around text
                height: 40px;
                color: #FFFFFF;
                background-color: #2C2C2C;  # Background color
            }
        """)
        
        # Add the search icon and QLineEdit to the layout
        main_layout.addWidget(search_icon)
        main_layout.addWidget(self.search_input)
        
        # Set a fixed height for the widget
        self.setFixedHeight(40)
        self.setStyleSheet("background-color: #2C2C2C; border-radius: 20px;")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchBar()
    window.show()
    sys.exit(app.exec_())
