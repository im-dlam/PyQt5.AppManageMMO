from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QVBoxLayout, QCheckBox
from PyQt5 import QtCore, QtGui

class CardWidget(QWidget):
    def __init__(self, title, note):
        super().__init__()
        self.setMinimumSize(QtCore.QSize(320, 200))
        self.setMaximumSize(QtCore.QSize(320, 200))

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(320, 200))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame.setStyleSheet("QFrame#frame{\n"
"background-color: rgb(77, 70, 115,200);\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(1, 10, 261, 31))
        self.frame_2.setStyleSheet("QFrame#frame_2{\n"
"background-color:rgba(78,72,116,255);\n"
"border-radius:5px;\n"
"}")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame_icons = QFrame(self.frame_2)
        self.frame_icons.setGeometry(QtCore.QRect(0, 0, 41, 31))
        self.frame_icons.setStyleSheet("image: url(:/icons/png/icons8-facebook-48.png);")
        self.frame_icons.setFrameShape(QFrame.StyledPanel)
        self.frame_icons.setFrameShadow(QFrame.Raised)
        self.frame_icons.setObjectName("frame_icons")
        self.label_title = QLabel(self.frame_2)
        self.label_title.setGeometry(QtCore.QRect(40, -1, 211, 31))
        font = QtGui.QFont()
        font.setFamily("MesloLGSDZ Nerd Font")
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_title.setObjectName("label_title")
        self.label_tag = QLabel(self.frame)
        self.label_tag.setGeometry(QtCore.QRect(270, 15, 81, 21))
        font = QtGui.QFont()
        font.setFamily("MesloLGSDZ Nerd Font")
        font.setBold(True)
        font.setWeight(75)
        self.label_tag.setFont(font)
        self.label_tag.setStyleSheet("color: rgb(255, 255, 255);\n"
"border-radius:5px;\n"
"background-color: rgb(128, 116, 255);")
        self.label_tag.setObjectName("label_tag")
        self.frame_3 = QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(1, 50, 350, 101))
        self.frame_3.setStyleSheet("QFrame#frame_3{\n"
"background-color:rgba(85,79,121,255);\n"
"border-radius:5px;\n"
"}")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.labe_note = QLabel(self.frame_3)
        self.labe_note.setGeometry(QtCore.QRect(6, 2, 341, 81))
        self.labe_note.setStyleSheet("color: rgb(255, 255, 255);")
        self.labe_note.setText("")
        self.labe_note.setObjectName("labe_note")
        self.checkBox = QCheckBox(self.frame)
        self.checkBox.setGeometry(QtCore.QRect(1, 160, 121, 31))
        font = QtGui.QFont()
        font.setFamily("MesloLGMDZ Nerd Font")
        font.setBold(True)
        font.setWeight(75)
        self.checkBox.setFont(font)
        self.checkBox.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color:rgba(85,79,121,255);\n"
"border-radius:5px;\n"
"padding:10px;")
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.frame)
