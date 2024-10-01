from PyQt5.QtWidgets import QApplication, QTableWidget, QPushButton, QVBoxLayout, QWidget

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Giả sử TableWidget đã tồn tại và có 3 hàng, 3 cột
        self.table_widget = QTableWidget(3, 3)  # Cấu trúc có sẵn
        
        # Thêm dữ liệu vào ô trước
        self.table_widget.setItem(0, 0, QTableWidgetItem("Row 0, Column 0"))
        self.table_widget.setItem(1, 1, QTableWidgetItem("Row 1, Column 1"))

        # Gọi hàm thêm nút vào ô
        self.add_button_to_table(1, 1)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

    def add_button_to_table(self, row, col):
        # Tạo nút button
        button = QPushButton("Click me")
        button.clicked.connect(self.on_button_click)
        
        # Kiểm tra nếu ô đã có widget hay chưa
        if not self.table_widget.cellWidget(row, col):
            # Nếu chưa có, thêm nút vào ô
            self.table_widget.setCellWidget(row, col, button)

    def on_button_click(self):
        print("Button clicked!")

# Tạo ứng dụng
app = QApplication([])
window = MyWindow()
window.show()

app.exec_()
