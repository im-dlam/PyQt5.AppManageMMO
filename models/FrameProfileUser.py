from main import *

class HoverLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super(HoverLabel, self).__init__(*args, **kwargs)
        self.setFixedSize(70,30)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
        QLabel {
                color: #c44dff;  /* Purple color */
                padding: 5px 10px;
                border-radius: 10px;
                text-decoration: none;  /* Remove underline */
            }
            QLabel:hover {
                background-color: #2d2d86;  /* Light purple hover effect */
            }
        """)
class AccountMenu(QWidget):
    def __init__(self, start_date, end_date, parent=None):
        super(AccountMenu, self).__init__(parent)
        
        self.start_date = start_date
        self.end_date = end_date
        
        # Create main layout
        main_layout = QVBoxLayout(self)
        
        # Center alignment for the profile section
        profile_layout = QHBoxLayout()
        profile_layout.setAlignment(Qt.AlignCenter)

        # Add profile picture (using a placeholder image)
        profile_pic = QLabel(self)
        pixmap = QPixmap(r'.\icons\png\e2537e3974afaef1f7be.jpg')  # Replace with the correct path to your profile image
        rounded_pixmap = self.get_rounded_pixmap(pixmap, 50)
        profile_pic.setPixmap(rounded_pixmap)
        
        # Add name and email
        name_email_layout = QVBoxLayout()
        name_email_layout.setAlignment(Qt.AlignCenter)

        # Create name layout to include the name and blue checkmark
        name_layout = QHBoxLayout()
        name_layout.setAlignment(Qt.AlignCenter)

        name = QLabel("Lâm Lê Đình", self)
        name.setFont(QFont("Arial", 12, QFont.Bold))
        name.setStyleSheet("color: rgb(235, 235, 235);")
        # Add blue checkmark next to the name (using a placeholder image for the checkmark)
        checkmark = QLabel(self)
        checkmark_pixmap = QPixmap(r'.\icons\png\tick_name')  # Replace with the correct path to your checkmark image
        checkmark.setPixmap(checkmark_pixmap.scaled(20, 15, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Add name and checkmark to the name layout
        name_layout.addWidget(name)
        name_layout.addWidget(checkmark)

        email = QLabel("ldl.booking@hotmail.com", self)
        email.setFont(QFont("Arial", 10))
        email.setStyleSheet("color: rgb(235, 235, 235);")
        email.setAlignment(Qt.AlignCenter)
        
        name_email_layout.addLayout(name_layout)
        name_email_layout.addWidget(email)
        
        profile_layout.addWidget(profile_pic)
        profile_layout.addLayout(name_email_layout)

        # Add Sign out action
        sign_out = HoverLabel("Sign out", self)
        sign_out.setFont(QFont("Arial", 9, QFont.Bold))
        sign_out.linkActivated.connect(self.sign_out_action)
        sign_out.mousePressEvent = self.sign_out_action  # Handle click event
        
        # Countdown timer
        # self.countdown_label = QLabel("", self)
        # self.countdown_label.setFont(QFont("Arial", 9))
        # self.countdown_label.setStyleSheet("color: rgb(235, 235, 235);")
        # self.countdown_label.setAlignment(Qt.AlignCenter)

        # Start the countdown timer
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_countdown)
        # self.timer.start(1000)  # Update every second
        
        # self.update_countdown()  # Initialize the countdown display
        
        # Add elements to main layout
        main_layout.addLayout(profile_layout)
        main_layout.addWidget(sign_out, alignment=Qt.AlignCenter)
        # main_layout.addWidget(self.countdown_label)
        
        self.setLayout(main_layout)
    
    def sign_out_action(self,event=None):
        print("Sign out clicked")

    def update_countdown(self):
        now = QDateTime.currentDateTime()
        remaining_time = self.end_date.toSecsSinceEpoch() - now.toSecsSinceEpoch()
        
        if remaining_time > 0:
            days = remaining_time // (24 * 3600)
            hours = (remaining_time % (24 * 3600)) // 3600
            minutes = (remaining_time % 3600) // 60
            seconds = remaining_time % 60
            countdown_text = f"{days}d-{hours}h-{minutes}m"
        else:
            countdown_text = "Expired"
        
        self.countdown_label.setText(countdown_text)


    def get_rounded_pixmap(self, pixmap, size):
        """Returns a rounded/circular pixmap."""
        rounded = QPixmap(size, size)
        rounded.fill(Qt.transparent)  # Make the background transparent

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addEllipse(0, 0, size, size)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        painter.end()

        return rounded