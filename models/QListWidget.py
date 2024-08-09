from main import *
import json 
# Tạo button trong horizontal
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
class CardWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.initUI(data)
    
    def setText(self):
        self.label_title.setText(self.title)
        self.label_tag.setText(self.type)
        self.label_tag.setAlignment(Qt.AlignCenter)
        self.labe_note.setText(self.note)
        f = QFont()
        f.setBold(True)
        self.labe_note.setFont(f)
        self.labe_note.setWordWrap(True)
        self.btn_addPlan.setText("OFF")
    def initUI(self, data):
        title, note , type  = data
        self.title = title
        self.note = note
        self.type = type

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(360, 200))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame.setStyleSheet("QFrame#frame{\n"
"background-color: rgb(38, 49, 98);\n"
"border-radius:10px; border: 0.5px solid #495b9e;\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(5, -1, 5, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_2.setStyleSheet("QFrame#frame_2{\n"
"background-color: rgb(38, 49, 98);\n"
"border-radius:5px;\n"
"}")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_3 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 10, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_icons = QFrame(self.frame_2)
        self.frame_icons.setMaximumSize(QtCore.QSize(40, 16777215))
        self.frame_icons.setStyleSheet("background-color: rgb(38, 49, 98);\n"
"image: url(:/icons/png/icons8-facebook-48.png);")
        self.frame_icons.setFrameShape(QFrame.StyledPanel)
        self.frame_icons.setFrameShadow(QFrame.Raised)
        self.frame_icons.setObjectName("frame_icons")
        self.horizontalLayout_3.addWidget(self.frame_icons)
        self.label_title = QLabel(self.frame_2)
        font = QFont()
        font.setFamily("MesloLGSDZ Nerd Font")
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(38, 49, 98);")
        self.label_title.setObjectName("label_title")
        self.horizontalLayout_3.addWidget(self.label_title)
        self.label_tag = QLabel(self.frame_2)
        self.label_tag.setMinimumSize(QtCore.QSize(100, 20))
        self.label_tag.setMaximumSize(QtCore.QSize(100, 20))
        font = QFont()
        font.setFamily("MesloLGSDZ Nerd Font")
        font.setBold(True)
        font.setWeight(75)
        self.label_tag.setFont(font)
        self.label_tag.setStyleSheet("color: rgb(103, 204, 187);\n"
"border-radius:5px;\n"
"background-color: rgb(55, 68, 119);")
        self.label_tag.setObjectName("label_tag")
        self.horizontalLayout_3.addWidget(self.label_tag)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QFrame(self.frame)
        self.frame_3.setStyleSheet("background-color: rgb(45, 59, 75);")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_4 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.labe_note = QLabel(self.frame_3)
        font = QFont()
        font.setFamily("MesloLGL Nerd Font")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.labe_note.setFont(font)
        self.labe_note.setStyleSheet("color: rgb(244, 243, 230);\n"
"background-color: rgb(38, 49, 98);\n"
"padding:4px;")
        self.labe_note.setObjectName("labe_note")
        self.horizontalLayout_4.addWidget(self.labe_note)
        self.verticalLayout.addWidget(self.frame_3)
        self.frame_4 = QFrame(self.frame)
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 35))
        self.frame_4.setStyleSheet("background-color: rgb(45, 59, 75);\n"
"border-top:1px solid  rgb(55, 68, 119);\n"
";")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_2 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_6 = QFrame(self.frame_4)
        self.frame_6.setStyleSheet("background-color: rgb(38, 49, 98);")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_2.addWidget(self.frame_6)
        self.frame_5 = QFrame(self.frame_4)
        self.frame_5.setStyleSheet("background-color: rgb(38, 49, 98);")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.btn_addPlan = QPushButton(self.frame_5)
        self.btn_addPlan.setGeometry(QtCore.QRect(90, 10, 75, 21))
        font = QFont()
        font.setFamily("MesloLGMDZ Nerd Font")
        font.setBold(True)
        font.setWeight(75)
        self.btn_addPlan.setFont(font)
        self.btn_addPlan.setStyleSheet("QPushButton#btn_addPlan{\n"
"color: rgb(103, 204, 187);\n"
"border-radius:5px;\n"
"    background-color: rgb(57, 74, 148);\n"
"}\n"
"QPushButton#btn_addPlan:hover{\n"
"border-radius:5px;\n"
"background-color: rgb(75, 94, 163);\n"
"}\n"
"")
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/png/icons8-dot-24_red.png"), QIcon.Normal, QIcon.Off)
        icon.addPixmap(QPixmap(":/icons/png/icons8-dot-24_live.png"), QIcon.Normal, QIcon.On)
        self.btn_addPlan.setIcon(icon)
        self.btn_addPlan.setIconSize(QtCore.QSize(20, 20))
        self.btn_addPlan.setCheckable(True)
        self.btn_addPlan.setObjectName("btn_addPlan")
        self.horizontalLayout_2.addWidget(self.frame_5)
        self.verticalLayout.addWidget(self.frame_4)
        self.horizontalLayout.addWidget(self.frame)

        self.setText()
        fileread = json.loads(open('./models/json/config.json','r',encoding='utf-8').read())
        if self.title.lower() in fileread["account.work"][self.type.lower()]:
            self.btn_addPlan.setText("ON")
            self.btn_addPlan.setChecked(True)
        


        self.btn_addPlan.clicked.connect(self.shows)
        self.setFixedSize(360, 200)  # Kích thước cố định cho từng item
    def shows(self):
        self.fileread = json.loads(open('./models/json/config.json','r',encoding='utf-8').read())
        if self.btn_addPlan.isChecked() == True:
            self.btn_addPlan.setText("ON")
            if self.title.lower() in self.fileread["account.work"][self.type.lower()]:
                return
            self.fileread["account.work"][self.type.lower()].append(self.title.lower())
            self.logfile()
        else:
            self.btn_addPlan.setText("OFF")
            if self.title.lower() in self.fileread["account.work"][self.type.lower()]:
                self.fileread["account.work"][self.type.lower()].remove(self.title.lower())
                self.logfile()
    

    def logfile(self):
        with open('./models/json/config.json' , "w" , encoding="utf-8") as f:
            json.dump(
                self.fileread,
                f,
                ensure_ascii=0,
                indent=4)
class SubjectQList:


        

    def ShowCardItems(self , widgets):
        widgets.WidgetFacebook.clear()
        widgets.WidgetFacebook.setSelectionMode(QListWidget.NoSelection)  # Tắt chọn hàng
        widgets.WidgetFacebook.setFocusPolicy(Qt.NoFocus)
        # Tạo các item WidgetFacebook và thêm vào QListWidget
        item = [
        ("Đăng Nhập Facebook","Tự động dăng nhập các tài khoản Facebook đã nhập ,dùng trình duyệt hỗ trợ antidetect bảo đảm an toàn khi login, tránh die tài khoản","Facebook"),
        ("Đăng Nhập Facebook (Cookie)","Tự động dăng nhập các tài khoản bằng cookie ,dùng trình duyệt hỗ trợ antidetect bảo đảm an toàn khi login, tránh die tài khoản","Facebook"),
        ("Giải Checkpoint 956","Tích hợp tự động giải Checkpoint dạng 956 của tài khoản , tự động lấy các mã qua email , hotmail , hỗ trợ imap , hỗ trợ giải captcha, tự động get cookie sau khi tài khoản LIVE .","Facebook"),
        ("Giải Checkpoint 282","Tích hợp tự động giải Checkpoint dạng 282 của tài khoản , tự động đá 282 nếu có , tự động up ảnh qua các nguồn ảnh , lấy số qua các site hỗ trợ , tự động giải captcha.","Facebook"),
        ("Đổi tên Facebook","Tự động đổi tên Việt random ngẫu nhiên theo giới tính tài khoản , hỗ trợ tên Việt có dấu .","Facebook"),
        ("Tương tác hàng ngày","Tự động tương tác feed random đọc , xem bài viết , xem bình luận như người thật , tự động check thông báo , chế độ này 80% chỉ LIKE bài viết , 20% còn lại sẽ tự động Comment và LIKE COMMENT","Facebook"),
        ("Đăng Bài Ngẫu nhiên","Tự động dăng bài lên feed , nhóm random ảnh , kèm ảnh , random nội dung , hỗ trợ nội dung có icons , hastag","Facebook"),
        ("Nhắn tin bạn bè","Nhắn tin với bạn bè trong danh sách gần nhất , hỗ trợ tương tác như người thật , đọc thông báo và nhắn tin","Facebook"),
        ("Xem Reel","Tự động xem reel theo đề xuất , đọc bình luần reel và like các comment 20%","Facebook"),
        ("Xem Video","Tự động xem Video theo đề xuất , đọc bình luần Video và like các comment 20%","Facebook"),
            ]
        item_names = [CardWidget(ix) for ix in item]  # Ví dụ với 12 item
        width = widgets.WidgetFacebook.width()
        item_width = 360
        item_spacing = 10
        items_per_row = width // (item_width + item_spacing)  # Tính toán số lượng item trên mỗi dòng

        if items_per_row == 0:
            items_per_row = 1

        for i in range(0, len(item_names), items_per_row):
            row_items = item_names[i:i + items_per_row]
            
            list_item_widget = ListWidgetItem(row_items, item_spacing, items_per_row)
            list_item = QListWidgetItem(widgets.WidgetFacebook)
            row_width = items_per_row * (item_width + item_spacing) - item_spacing
            list_item.setSizeHint(QSize(row_width, 250))  # Kích thước cho mỗi dòng chứa items
            widgets.WidgetFacebook.setItemWidget(list_item, list_item_widget)