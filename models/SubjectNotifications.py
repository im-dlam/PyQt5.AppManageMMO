from main import *


class Notification(QWidget):
    def __init__(self, parent=None):
        super(Notification, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.parent = parent
        

        self.label = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)


    # Set initial opacit
    # ///////////////////////////////
    # set css
    def _notification_box(self , success):
        if success:
            scrip = """
            QLabel {
                background-color: #79D5BF;
                color: #E6EEEC;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            """
        else:
            scrip = """
            QLabel {
                background-color: #E2839B;
                color: #E6EEEC;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;

            }
            """
        self.label.setStyleSheet(scrip)
        font = QFont('MesloLGLDZ Nerd Font', 8)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setWordWrap(True)  # Enable word wrapping
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(4, 4)
        self.label.setGraphicsEffect(shadow)
    # ///////////////////////////////
    # thêm tin nhắn vào thanh thông báo

    def SendMsg(self, tweet ):
        msg, success = tweet
        duration, x_offset, y_offset, width = 3000 , 20 , 20 , 200
        # /////////////////////
        # trạng thái thành công
        self._notification_box(success)

        # ////////////////////////////////
        # thêm tin nhắn
        self.label.setText(msg)

        self.label.setFixedWidth(width)  # Set fixed width to enable word wrap
        self.adjustSize()
        
        self.move_notification(x_offset, y_offset)
        
        self.show()
        QTimer.singleShot(duration, self.hide)
    
    def move_notification(self, x_offset=20, y_offset=20):
        parent_rect = self.parent.rect()
        x = parent_rect.width() - self.width() - x_offset
        y = parent_rect.height() - self.height() - y_offset
        self.move(self.parent.mapToGlobal(parent_rect.topLeft()) + QPoint(x, y))
        