from main import *


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
        pixmap = QPixmap(r'D:\UI Python\GUI_PyQt5_My_App\icons\png\e2537e3974afaef1f7be.jpg')  # Replace with the correct path to your profile image
        profile_pic.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
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
        checkmark_pixmap = QPixmap(r'D:\UI Python\GUI_PyQt5_My_App\icons\png\tick_name')  # Replace with the correct path to your checkmark image
        checkmark.setPixmap(checkmark_pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))

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
        sign_out = QLabel("<a href='#'>Sign out</a>", self)
        sign_out.setFont(QFont("Arial", 10))
        sign_out.setStyleSheet("color: rgb(235, 235, 235);")
        sign_out.setTextInteractionFlags(Qt.TextBrowserInteraction)
        sign_out.setOpenExternalLinks(False)
        sign_out.setAlignment(Qt.AlignCenter)
        sign_out.linkActivated.connect(self.sign_out_action)
        
        # Countdown timer
        self.countdown_label = QLabel("", self)
        self.countdown_label.setFont(QFont("Arial", 10))
        self.countdown_label.setStyleSheet("color: rgb(235, 235, 235);")
        self.countdown_label.setAlignment(Qt.AlignCenter)

        # Start the countdown timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)  # Update every second
        
        self.update_countdown()  # Initialize the countdown display
        
        # Add elements to main layout
        main_layout.addLayout(profile_layout)
        main_layout.addWidget(sign_out)
        main_layout.addWidget(self.countdown_label)
        
        self.setLayout(main_layout)
    
    def sign_out_action(self):
        print("Sign out clicked")

    def update_countdown(self):
        now = QDateTime.currentDateTime()
        remaining_time = self.end_date.toSecsSinceEpoch() - now.toSecsSinceEpoch()
        
        if remaining_time > 0:
            days = remaining_time // (24 * 3600)
            hours = (remaining_time % (24 * 3600)) // 3600
            minutes = (remaining_time % 3600) // 60
            seconds = remaining_time % 60
            countdown_text = f"{days}d {hours}h {minutes}m {seconds}s remaining"
        else:
            countdown_text = "Time expired"
        
        self.countdown_label.setText(countdown_text)