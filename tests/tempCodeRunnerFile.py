import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xác Nhận Xóa")
        self.setGeometry(100, 100, 300, 200)

        # Đặt nền màu đen xanh cho cửa sổ chính
        self.setStyleSheet("background-color: #001F3F;")  # Mã màu cho dark blue

        self.delete_button = QPushButton("Delete", self)
        self.delete_button.setGeometry(100, 80, 100, 30)
        self.delete_button.clicked.connect(self.show_confirmation)

    def show_confirmation(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Xác Nhận')
        msg_box.setText("Bạn có chắc chắn muốn xóa không?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setStyleSheet("background-color: #001F3F; color: white;")  # Nền và màu chữ của hộp thoại

        reply = msg_box.exec_()

        if reply == QMessageBox.Yes:
            print("Đã xóa.")
        else:
            print("Không xóa.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
