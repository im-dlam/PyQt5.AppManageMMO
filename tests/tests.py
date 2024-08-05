import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QListWidget, QListWidgetItem, 
                             QCheckBox, QLineEdit, QPushButton, QFrame, QSizePolicy, QSpacerItem)
from PyQt5.QtCore import Qt, QSize

class CardWidget(QWidget):
    def __init__(self, title, note):
        super().__init__()
        self.initUI(title, note)
        
    def initUI(self, title, note):
        layout = QVBoxLayout()
        
        # Tạo frame
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame_layout = QVBoxLayout()
        
        # Tạo nút bấm
        button = QPushButton("Button")
        
        # Tạo checkbox và label
        checkbox = QCheckBox()
        checkbox.setText(title)
        checkbox.setTristate(False)
        
        # Tạo QLineEdit để ghi chú có thể sửa đổi
        note_edit = QLineEdit(note)
        
        # Thêm button, checkbox và QLineEdit vào frame layout
        frame_layout.addWidget(button)
        frame_layout.addWidget(checkbox)
        frame_layout.addWidget(note_edit)
        
        frame.setLayout(frame_layout)
        
        # Thêm frame vào layout chính của CardWidget
        layout.addWidget(frame)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QFrame {
                background-color: #2E2E2E;
                color: #FFFFFF;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
            }
            QLineEdit {
                background-color: #444;
                color: #FFF;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton {
                background-color: #444;
                color: #FFF;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px;
            }
        """)

        # Đặt kích thước cố định cho widget
        self.setFixedSize(300, 200)  # Kích thước cố định cho từng item

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resizable Items Example")
        self.setGeometry(100, 100, 900, 600)
        self.initUI()
        
    def initUI(self):
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.NoSelection)  # Tắt chọn hàng

        # Thêm các item vào QListWidget
        self.cards = [CardWidget(f"Title {i + 1}", f"Note {i + 1}") for i in range(10)]
        self.populate_list_widget()

        self.main_layout.addWidget(self.list_widget)
        self.main_widget.setLayout(self.main_layout)
        
        self.setCentralWidget(self.main_widget)

    def populate_list_widget(self):
        self.list_widget.clear()
        width = self.list_widget.width()
        item_width = 300
        item_spacing = 10
        items_per_row = width // (item_width + item_spacing)  # Tính toán số lượng item trên mỗi dòng

        if items_per_row == 0:
            items_per_row = 1

        for i in range(0, len(self.cards), items_per_row):
            row_items = self.cards[i:i + items_per_row]
            
            list_item_widget = ListWidgetItem(row_items, item_spacing, items_per_row)
            list_item = QListWidgetItem(self.list_widget)
            row_width = items_per_row * (item_width + item_spacing) - item_spacing
            list_item.setSizeHint(QSize(row_width, 220))  # Kích thước cho mỗi dòng chứa items
            self.list_widget.setItemWidget(list_item, list_item_widget)
    
    def resizeEvent(self, event):
        self.populate_list_widget()
        super().resizeEvent(event)

class ListWidgetItem(QWidget):
    def __init__(self, widgets, spacing, items_per_row):
        super().__init__()
        self.initUI(widgets, spacing, items_per_row)
        
    def initUI(self, widgets, spacing, items_per_row):
        layout = QHBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)
        if len(widgets) < items_per_row:
            layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.setSpacing(spacing)  # Khoảng cách giữa các item
        layout.setAlignment(Qt.AlignLeft)  # Căn chỉnh các item sang trái
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
