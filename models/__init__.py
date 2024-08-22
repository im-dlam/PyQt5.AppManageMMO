
from PyQt5.QtCore import (
    QCoreApplication , Qt , QAbstractAnimation ,
    QDateTime, QAbstractListModel, QTimer , QAbstractTableModel , QAnimationGroup,
    QFile,QEvent, QThread, pyqtSignal , QModelIndex , QSize , QPoint , QElapsedTimer,
    QRect , QRectF , 
    )
from PyQt5.QtGui import (
    QColor , QClipboard , QCloseEvent , QCursor , QFont , QFontMetrics,
    QDrag , QIcon , QMovie , QMouseEvent , QPainter , QPixmap , QPainterPath,
    QBrush , QPalette , QRegion , 
    
    
)
from PyQt5.QtWidgets import (
    QAbstractButton , QAbstractGraphicsShapeItem , QGraphicsDropShadowEffect ,
    QAbstractItemView , QAbstractItemDelegate , QAction , QCheckBox , QComboBox,
    QFileDialog , QFrame , QGraphicsGridLayout , QBoxLayout , QWidget, QProxyStyle,
    QScrollBar , QHeaderView , QStyledItemDelegate , QStyleOptionViewItem , QMenu ,
    QLabel , QApplication , QVBoxLayout , QToolButton , QHBoxLayout , QTableWidgetItem,
    QWidgetAction, QListWidget , QPushButton , QListWidgetItem , QTableWidget,
    QStyle , QSpacerItem , QSizePolicy ,
    
)
from PyQt5.QtMultimedia import (
    QAudio
)
from . QtWidgetsButton import  AnimatedToggle

from . app import *
from . Config import *
# call models
from . Ui_Functions import *
from . SubjectTools import *
from . SubjectNotifications import *
from . SubjectQtables import *
from . QListWidget import *
from . FrameProfileUser import *
from . SubjectTemps import *
from . SubjectTime import *
from . SubjectScrips import *


from . sql import *
from . SubjectFileName import *
from . SubjectRighClick import *

from . html  import *
from . SubjectQThread import *


# import selenium

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from . SubjectAutoBrowser import *


from functools import partial