from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton

class TableDemo(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.table = QTableWidget(5, 3)  # 5 hàng và 3 cột

        # Thêm dữ liệu mẫu
        for i in range(5):
            for j in range(3):
                self.table.setItem(i, j, QTableWidgetItem(f"Item {i+1}-{j+1}"))

        self.layout.addWidget(self.table)

        # Tạo nút xóa
        self.delete_button = QPushButton("Xóa hàng")
        self.delete_button.clicked.connect(self.delete_row)
        self.layout.addWidget(self.delete_button)

        self.setLayout(self.layout)

    def delete_row(self):
        selected_row = self.table.currentRow()  # Lấy chỉ số hàng được chọn
        if selected_row >= 0:
            self.table.removeRow(selected_row)  # Xóa hàng

app = QApplication([])
window = TableDemo()
window.show()
app.exec_()
