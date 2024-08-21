import sys , os

#######################################################################################
# functions 
from models import * 
from widgets import *
widgets , resize  , processing_thread , msg  = None , None , None , None 

DataProcessingFill  , DataFillProcess = (None , None) , None

text = '''

version = object
#######################################################################################
# index theo thứ tự bảng table

class WindowInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAutoFillBackground(True)
        # Apply the stylesheet
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.resize(700, 699)
        #######################################################################################
        # call item * 
        global widgets , DataProcessingFill , msg , index_name , DataFillProcess 
        #######################################################################################
        self.is_left_mouse_pressed = False
        self.first_selected_item =  None 
        self.total_items, self.batch_size, self.current_batch = int(1e7) , 500 , 0

        #######################################################################################


        #######################################################################################
                                                # Hiển thị trong centralwidget của app
        self.setMinimumSize(QSize(1270, 0))
        widgets , msg = self.ui , Notification(self.ui.centralwidget)

        self.setWindowTitle("BeSyn - Quản Lý Đa Nền Tảng Tài Khoản")
        #######################################################################################


        #######################################################################################
        # Tự động dịch chuyển thanh thông báo phù hợp khi phóng to , thu nhỏ ứng dụng
        self.resizeEvent_ = self._on_resize
        #######################################################################################
        # button list array

        self.buttons_ = ObjectTemp.TempsButtonTextWidgets(self , widgets)
        self.buttons_icons = ObjectTemp.TempsButtonIconsWidgets(self , widgets)
        
        #######################################################################################
        self.buttons_tools = ObjectTemp.TempsButtonToolsWidgets(self , widgets)
            
        FrameRightClick(widgets,self)

        #######################################################################################
        # thêm nút cho table widget
        widgets.TableManage.setHorizontalHeader(CustomHeaderHorizontal(self))
            
        #######################################################################################
        """
            Mouse resize
        """
        self.RemoveWindowFlags()

        #######################################################################################
        # Replace central widget with the custom one
        # widgets.centralwidget.setStyleSheet(central_script.format(10))
        
        # Subject connect các button
        self.SubjectConnectButton()

        #######################################################################################
        # Load các lệnh về Ui_Functions

        self.SubjectFunctions()


        #######################################################################################
        # custom shadow frame

        #######################################################################################
        # Tạo HeaderHorizontal
        self.SubjectSetupTableManage()


        #######################################################################################
        # turn off focus
        QTableTools.remove_focus(self, widgets.TableManage)

        # Tự đồng tạo danh mục mặc định và load item lên combobox danh mục
        self.SQLProcessing()

        #######################################################################################/
        # Tạo cột tiêu đề nằm ngang | 14 cột
        

        #######################################################################################
        # custom scroll TableManage
        # widgets.TableManage.setHorizontalHeaderItem()
        # CustomScrollBar : thêm hiệu ứng thanh cuộn cho các tablewidget
        widgets.TableManage.setVerticalScrollBar(CustomScrollBar(widgets.TableManage, Qt.Vertical))
        widgets.TableManage.setHorizontalScrollBar(CustomScrollBar(widgets.TableManage, Qt.Horizontal))



        #######################################################################################
        # phần này tạo button có hình đại diện , thêm hiệu ứng đăng xuất , thông tin profile tóm tắt
        self.MenuButtonProfileUser()


        #######################################################################################
        # thêm model cho table widget
        self.SubjectAutoLoadData()


        #######################################################################################
        # mô phỏng chế độ kéo dãn cho các cột
        self.InteractiveHeader()


        #######################################################################################
        # Tạo icons hiển thị con trỏ kéo dãn màn hình
        self.EdgeGripShort()
        #######################################################################################
        # search
        self.lastSearchTime = QElapsedTimer()
        self.lastSearchTime.start()  # Khởi động bộ đếm thời gian
        widgets.line_search.textChanged.connect(self.search)


        #######################################################################################
        # Load dữ liệu
        self.ComboboxFileActivedConnect()


        #######################################################################################
        widgets.ComboboxFile.activated.connect(self.ComboboxFileActivedConnect)

        widgets.TableManage.selectionModel().selectionChanged.connect(self.MouseClickCheckBox)

        widgets.TableManage.cellClicked.connect(self.ShiftAutoCheckbox)

        widgets.TableManage.cellClicked.connect(self.CheckBoxCount)

        #######################################################################################

        widgets.TableManage.cellDoubleClicked.connect(lambda row , column,widgets=widgets:QTableTools.CopyColumnContentDoubleClick(self , widgets , row , column))
        self.show()



        #######################################################################################
        # END 
        #######################################################################################





    def CheckBoxCount(self,row, column ):
        total = 0
        for i in range(widgets.TableManage.rowCount()):
            checkbox = widgets.TableManage.item(i, 0)
            if checkbox.checkState() == 2:
                total += 1
        
        widgets.label_select.setText(str(total))
        widgets.label_running.setText(f"0 / {total}")
    #######################################################################################
    # đổi trạng thái checkbox khi người dùng nhấn SHIFT để chọn các dòng
    def ShiftAutoCheckbox(self, row, column ):
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            if self.first_selected_item is not None:
                first_row, first_col = self.first_selected_item
                widgets.TableManage.clearSelection()
                for r in range(min(first_row, row), max(first_row, row) + 1):
                    for c in range(min(first_col, column), max(first_col, column) + 1):
                        #######################################################################################
                        # r : rows 
                        item = widgets.TableManage.item(r, 0)
                        #######################################################################################
                        # set Checked
                        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                        item.setCheckState(Qt.Checked)
        else:
            self.first_selected_item = (row, column)

    #######################################################################################
    # click frame auto set checked
    def MouseClickCheckBox(self , index):

        for obj in index.indexes():
            if obj.column() == 0:
                item =widgets.TableManage.item(obj.row(), 0)
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                item.setCheckState(Qt.Checked)

    def SubjectFunctions(self):
        #######################################################################################
        # toggle checked auto refresh
        # toggle button text , icons 

        # chuyển đổi css cho các nút ở menu
        Functions.SwitchButtonCssChecked(self ,self.buttons_) # button text

        #######################################################################################
        # các nút icons khi ẩn menu
        Functions.SwitchButtonToolsCssChecked(self ,self.buttons_icons) # button icons

        #######################################################################################
        # các nút tools ở home
        Functions.SwitchButtonToolsCssChecked(self ,self.buttons_tools)

        Functions.ButtonPlaySound(self , self.buttons_tools)
        #######################################################################################
        # xử lý tự đổi trạng thái khi người dùng click vào ô frame chứa checkbox
        Functions.AutoSwitchCheckboxStatus(self , widgets)

        #######################################################################################
        # customs css cho btn_profile ở task top
        # sound opening
        Functions.OpenSoundApp(self)

        Functions.ShadowFrameConditional(self, widgets.frame_taskbar,QColor(0,10,10,100))



    def SubjectSetupTableManage(self):
        QTableTools.SubjectNewHorizontalHeader(self , widgets)


        QTableTools.SubjectHiddenColumn(self , widgets)

        #######################################################################################
        # giới hạn chiều rộng của cột
        QTableTools.SetColumnWidthTableWidget(self , widgets)

    #######################################################################################
    # Subject connect các button
    def SubjectConnectButton(self):

        Functions.ShadowFrameConditional(self,widgets.SettingPage,QColor(0,10,10,100))
        
        FrameID =  [widgets.FrameID_ProfileLog , widgets.FrameID_AutoSortSize,
                    widgets.FrameID_Backup,widgets.FrameID_BrowserOptimization,
                    widgets.FrameID_Proxy1,widgets.FrameID_Proxy2,widgets.FrameID_ContentChatGpt,
                    widgets.FrameID_ChromeHeadless]
        Functions.AnimatedToggleButton(self , FrameID)
        #######################################################################################
        widgets.btn_hide.clicked.connect(lambda: Functions.AnimationSwitchMenu(self, widgets))
        widgets.btn_hide_icons.clicked.connect(lambda: Functions.AnimationSwitchMenu(self, widgets))
        #######################################################################################

        widgets.btn_maximum.clicked.connect(lambda: Functions.ResizeMode(self, widgets))
        widgets.btn_minimum.clicked.connect(lambda: self.showMinimized())

        widgets.btn_close.clicked.connect(lambda: self.close())

        #######################################################################################
        # Functions button clicked connect

        widgets.btn_add.clicked.connect(self.window_additem)
        widgets.btn_proxy.clicked.connect(self.window_proxies)

        #######################################################################################
        # load lại dữ liệu
        widgets.btn_refresh.clicked.connect(self.ComboboxFileActivedConnect)

        #######################################################################################
        # cài dặt kịch bản
        widgets.btn_plan_tool.clicked.connect(self.WidgetFrameScheme)
        widgets.btn_plan_tool_icons.clicked.connect(self.WidgetFrameScheme)


        widgets.btn_all.clicked.connect(self.SwapWidgetFrameHome)
        widgets.btn_all_icons.clicked.connect(self.SwapWidgetFrameHome)


        # cài đặt chung
        widgets.btn_setting.clicked.connect(self.WidgetFrameSetting)
        widgets.btn_setting_icons.clicked.connect(self.WidgetFrameSetting)

        # chuyển đổi back giữa các frame
        self.SwapWidgetFrameHome()
        widgets.btn_back.clicked.connect(self.SwapWidgetFrameHome)
        widgets.btn_back_2.clicked.connect(self.SwapWidgetFrameHome)

        #######################################################################################
        # lưu cài đặt và hiển yhij thông báo thành công
        widgets.btn_settingSave.clicked.connect(self.ProcessConfigSetting)

    #######################################################################################
    # chuyển đổi frame màn hình của stack widget
    # Màn hình quản lý 
    #######################################################################################
    def SwapWidgetFrameHome(self):
        widgets.stackedWidget.setCurrentWidget(widgets.HomePage)
    


    #######################################################################################
    # Màn hình kịch bản
    def WidgetFrameScheme(self):
        widgets.stackedWidget.setCurrentWidget(widgets.PlanPage)

        SubjectQList.ShowCardItems(self , widgets)



    #######################################################################################
    # Màn hình cài đặt chung
    def WidgetFrameSetting(self):
        widgets.stackedWidget.setCurrentWidget(widgets.SettingPage)



    #######################################################################################
    # Xóa thanh tiêu đề và xử lý di chuyển
    def RemoveWindowFlags(self):

        #######################################################################################
        # màu nền của giao diện chính về ban đầu
        #######################################################################################

        self.setAttribute(Qt.WA_TranslucentBackground) 

        #######################################################################################
        # xử lý di chuyển ứng dụng
        self.resize = Resize(self)



    #######################################################################################
    # Tự đồng tạo danh mục mặc định và load item lên combobox danh mục
    def SQLProcessing(self):
        #######################################################################################
        # SQL
        # tạo thư mục mặc định
        SubjectSQL.CreateTableNew(self, name= "ALL",widgets=widgets)

        #######################################################################################
        SubjectProcessFile.LoadNameTabelSQL(self , widgets)

        #######################################################################################
    

    #######################################################################################
    # phần này tạo button có hình đại diện , thêm hiệu ứng đăng xuất , thông tin profile tóm tắt

    def MenuButtonProfileUser(self):
        # Functions.set_icons(self , widgets)
        start_date = QDateTime.currentDateTime()
        menubar = self.menuBar()
        end_date = start_date.addDays(7)  # Example: 7 days from now
        contextMenu = CustomMenuProfile(self)
        account_widget = AccountMenu(start_date, end_date, self)
        action = QWidgetAction(self)
        action.setDefaultWidget(account_widget)
        contextMenu.addAction(action)
        contextMenu.addSeparator()
        
        # Add additional menu items
        manage_action = QAction('Manage account and devices', self)
        payment_action = QAction('Payment methods', self)
        redeem_action = QAction('Redeem code or gift cards', self)
        settings_action = QAction('Settings', self)
        
        contextMenu.addAction(manage_action)
        contextMenu.addAction(payment_action)
        contextMenu.addAction(redeem_action)
        contextMenu.addAction(settings_action)
        
        menubar.addMenu(contextMenu)
        widgets.btn_profile.setMenu(contextMenu)

    
    #######################################################################################

    ######################################################################################
    # Căn chỉnh màn hình phụ ở chính giữa giao diện APP
    def center(self , widgets_ui):
        # Lấy kích thước của màn hình chính
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Lấy kích thước của cửa sổ
        window_geometry = widgets_ui.frameGeometry()

        # Tính toán vị trí để cửa sổ ở giữa màn hình
        x = (screen_geometry.width() - window_geometry.width() + 50) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2

        # Di chuyển cửa sổ đến vị trí tính toán
        widgets_ui.move(x, y)

    #######################################################################################
    # Màn Hình Thêm Dữ Liệu
    def window_additem(self):
        # code sql/300
        
        Namecategory =  widgets.ComboboxFile.currentText()
        NameaccountType =  widgets.ComboBoxTypeAccount.currentText()


        #######################################################################################
        # Call Functions Connect UI
        # Chức năng hiển thị GUI thêm dữ liệu tài khoản
        # Call Sub from Functions Show UI Clone
        window_widgets , windows_ui = Ui_Connect.show_ui(self, Ui_TabWidget)
        window_widgets.tabWidget.setCurrentIndex(0)

        #######################################################################################
        # căn giữa
        self.center(windows_ui)

        #######################################################################################
        # toggle frame, button to shadow
        # chỉnh sửa làm bóng các frame
        Functions.ShadowFrameConditional(self , window_widgets.label , QColor(0,0,10,40))
        Functions.ShadowFrameConditional(self , window_widgets.frame_3 , QColor(0,0,10,40))
        Functions.ShadowFrameConditional(self , window_widgets.frameMain , QColor(10,0,10,80))
        Functions.ShadowFrameConditional(self , window_widgets.frame_8 , QColor(0,0,10,40))
        Functions.ShadowFrameConditional(self , window_widgets.frame_5 , QColor(0,0,10,40))
        Functions.ShadowFrameConditional(self , window_widgets.item_close , QColor(0,0,10,40))
        Functions.ShadowFrameConditional(self , window_widgets.item_add , QColor(0,0,10,60))

        #######################################################################################


        #######################################################################################
        # Xử lý thao tác click Button trong giao diện chính
        self.SubjectDataProcessingQThread = SubjectDataProcessing(window_widgets)
        self.SubjectDataProcessingQThread.signal.connect(self.signalSubjectDataProcessing)
        window_widgets.plain_item.textChanged.connect(self.startSubjectDataProcessing)

        window_widgets.item_add.clicked.connect(lambda : self.SubjectDataProcessingConfirm(window_widgets , windows_ui))
        window_widgets.item_close.clicked.connect(lambda : windows_ui.close())
        window_widgets.item_close.clicked.connect(lambda: self.RemoveWindowFlags())

        # Thêm Text và Xóa để hiện Placehoder
        window_widgets.plain_item.setPlaceholderText("Nhập tài khoản ...")
        window_widgets.plain_item.setPlainText("...")
        window_widgets.plain_item.clear()
        #######################################################################################
        # add list folder
        items = SubjectSQL.GetSQLTable(self) # Lấy danh sách tên trong cơ sở dữ liệu
        items.remove("ALL")
        window_widgets.combo_danhmuc.addItems(items)
        window_widgets.combo_danhmuc.setCurrentText(Namecategory)

        window_widgets.combo_account.setCurrentText(NameaccountType)
        window_widgets.combo_ua.setCurrentText("Windows")

        # Apply blur effect before showing the window
        windows_ui.show()

        # Remove blur effect when window is closed

    #######################################################################################
    # chạy QThread xử lý định dạng dữ liệu và gán cho DataProcessingFill
    def startSubjectDataProcessing(self):
        if not self.SubjectDataProcessingQThread.isRunning():
            self.SubjectDataProcessingQThread.start()
    def signalSubjectDataProcessing(self , data : tuple):
        global DataProcessingFill 
        DataProcessingFill = data

    #######################################################################################
    # phần này xử lý dữ liệu nhập , dùng QThread tránh GUI Lag
    def SubjectDataProcessingConfirm(self , window_widgets , window_ui):
        global DataProcessingFill , processing_thread
        #######################################################################################
        # list functions combox item
        # code 200
        self.RemoveWindowFlags()
        self.NameCategory = window_widgets.combo_danhmuc.currentText()
        if window_widgets.plain_item.toPlainText() == "":
            msg.SendMsg(
                ("Vui lòng nhập dữ liệu !",          0)
                )
            window_ui.close()
            return
        
        _widgets = ObjectTemp.TempsComboBoxAddItems(self , window_widgets)
        
        textCurrent = []

        for widgets_c in _widgets:
            textCurrent.append(widgets_c.currentText())
        
        #######################################################################################
        # xử lý dữ liệu và gửi tới hàm on_processing
        
        processing_thread = ProcessingThread(window_widgets , DataProcessingFill , textCurrent)

        #######################################################################################
        # truyền dữ liệu tới OnProcessingFinished() khi hoàn thành xong task và show lên table
        processing_thread.processing_finished.connect(self.OnProcessingDataFinished)
        processing_thread.start()

        #######################################################################################
        # đòng cửa sổ nhập
        window_ui.close()


    #######################################################################################
    # xóa các dữ liệu hiển thị và thêm dữ liệu ở mục chỉ định
    def ComboboxFileActivedConnect(self):
        global DataFillProcess
        
        widgets.TableManage.clear()
        #######################################################################################
        # Config lại headerhorizontal 
        self.SubjectSetupTableManage()
        self.total_items, self.batch_size, self.current_batch = int(1e7) , 500 , 0
        if widgets.ComboboxFile.currentText() == "ALL":
            ListName = SubjectSQL.GetSQLTable(self)
        else:
            ListName = [widgets.ComboboxFile.currentText()]
        DataFillProcess = SubjectProcessFile.GetDataFromTable(self , ListName)
        #########################################
        # Xử lý QThread , hiển thị 500 dữ liệu 
        #########################################
        self.ProcessingQThreadDataItemsCondition(DataFillProcess)

        Functions.UpdateLabelTotalAccount(self , widgets , len(DataFillProcess))

    
    #######################################################################################
    # Dữ liệu ở hàm SubjectDataProcessingConfirm() chạy QThread xong sẽ truyền tới hàm này
    #######################################################################################
    def OnProcessingDataFinished(self , res : dict, widgets_ : object):
        global DataFillProcess
        #######################################################################################
        # gán dữ liệu đã xử lý để gửi tới hàm thêm dữ liệu
        DataFillProcess = res
        self.maxTotal =  len(DataFillProcess)
        Functions.UpdateLabelTotalAccount(self , widgets , len(DataFillProcess))
        #######################################################################################
        # insert dữ liệu vào table
        self.SubjectOnProcessinginsertDataFinished = SubjectOnProcessingDataFinished(widgets, self.NameCategory , DataFillProcess)
        self.startOnProcessingDataFinished()
        #######################################################################################
        # lấy 500 dữ liệu đầu tiên và hiển thị , tránh lag gui
        self._GetDataThread = GetDataThread(widgets, self.NameCategory , self.maxTotal)
        self._GetDataThread.signal.connect(self.signalOnProcessingDataFinished)
        self.starGetDataThread()

        msg.SendMsg(("Load dữ liệu có thể mất chút thời gian !!!",1))

                                #       , Ui_main , [{},{} ...]      , ["","" ...]

    #######################################################################################
    # lấy dữ liệu xử lý định dạng phù hợp để truyền tới add item vào QTabel
    #######################################################################################
    def signalOnProcessingDataFinished(self , data : list):
        global DataFillProcess 
        DataFillProcess = data
        # self.ProcessingQThreadDataItemsCondition(DataFillProcess)
        self.ComboboxFileActivedConnect()
        #######################################################################################
        # cập nhật thông số tài khoản

        if len(DataFillProcess) == self.maxTotal:
            msg.SendMsg(("Thêm thành công !",                1))
        else:
            msg.SendMsg(("Đang load dữ liệu !",                1))

    #######################################################################################
    # QThread tránh lỗi isrunning
    #######################################################################################
    def starGetDataThread(self):
        if not self._GetDataThread.isRunning():
            self._GetDataThread.start()

    def startOnProcessingDataFinished(self):
        if not self.SubjectOnProcessinginsertDataFinished.isRunning():
            self.SubjectOnProcessinginsertDataFinished.start()

    #######################################################################################
    # Gui hiển thị dữ liệu nhập Proxy . dùng Tabwidget và chuyển đổi sang index : 1
    #######################################################################################
    def window_proxies(self):
        #######################################################################################
        
        window_widgets , windows_ui = Ui_Connect.show_ui(self, Ui_TabWidget)
        window_widgets.tabWidget.setCurrentIndex(1)
        self.center(windows_ui)
        # window_widgets -> Object : sử dụng để gọi các frame , button ...
        # window_ui      -> OBject : sử dụng để close , show , công dụng như hàm self.show()
        # Call Functions Connect UI
        self.item_CheckProxy_Change  =  False 
        #######################################################################################
        # Call Sub from Functions Show UI Clone PROXIES
        # window_widgets.item_add.clicked.connect(lambda : self.SubjectDataProcessingConfirm(window_widgets , windows_ui))
        window_widgets.item_closeProxy.clicked.connect(lambda : windows_ui.close())
        window_widgets.item_closeProxy.clicked.connect(lambda: self.RemoveWindowFlags())
        #######################################################################################
        # ẩn QPlainText

        window_widgets.plain_Proxy.hide()

        window_widgets.item_import.clicked.connect(lambda:self.showPlainProxy(window_widgets))
        window_widgets.item_CheckProxy.clicked.connect(lambda:self.ShowTabelProxy(window_widgets))
        #######################################################################################
        # run , check script


    def ShowTabelProxy(self,window_widgets):
        if self.item_CheckProxy_Change:
            window_widgets.plain_Proxy.hide()
            self.item_CheckProxy_Change = False
            window_widgets.item_import.setText("import")
            window_widgets.item_CheckProxy.setText("Check Proxy")
            window_widgets.item_import.setStyleSheet(scripProxyImport)

    def showPlainProxy(self , window_widgets):
        window_widgets.plain_Proxy.show()
                # Thêm Text và Xóa để hiện Placehoder
        window_widgets.plain_Proxy.setPlaceholderText("Nhập Proxy ...")
        window_widgets.plain_Proxy.setPlainText("...")
        window_widgets.plain_Proxy.clear()


        # change status button
        window_widgets.item_import.setText("Thêm")
        window_widgets.item_import.setStyleSheet(scripProxyAdd)
        
        ####################################
        # change status back
        window_widgets.item_CheckProxy.setText("Quay lại")
        self.item_CheckProxy_Change = True 
    #######################################################################################
    # phần này xử lý di chuyển chuột và kéo dãn màn hình ứng dụng , hiện tại chưa xử lý thêm
    def resizeEvent(self, event):
        super().resizeEvent(event)
        rect = widgets.centralwidget.rect()
        SubjectQList.ShowCardItems(self , widgets)
        grip_width = 7  # Độ rộng của EdgeGrip
        self.left_grip.setGeometry(0, 0, grip_width, rect.height())
        self.right_grip.setGeometry(rect.width() - grip_width, 0, grip_width, rect.height())
        self.top_grip.setGeometry(0, 0, rect.width(), grip_width)
        self.bottom_grip.setGeometry(0, rect.height() - grip_width, rect.width(), grip_width)

    #######################################################################################
    # phần điều kiện chuột tự di chuyển
    def mousePressEvent(self, event):
        # Check if the mouse press is within the frameID widget
        if event.button() == Qt.LeftButton and not widgets.main_screen.geometry().contains(event.pos()) or (event.button() == Qt.LeftButton and  widgets.frame_taskbar.geometry().contains(event.pos())):
            self.is_left_mouse_pressed = True
            self.resize.mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton :
            self.is_left_mouse_pressed = False
            self.resize.mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_left_mouse_pressed and self.isMaximized():
            self.is_left_mouse_pressed = False
            self.showNormal()
        self.resize.mouseMoveEvent(event)

    
    #######################################################################################
    # hiệu ứng làm tròn viền
    def paintEvent(self, event):
        painter = QPainter(self)
        path = QPainterPath()
        if self.isMaximized():
            #######################################################################################
            # full màn và cạnh nhọn
            #######################################################################################
            path.addRoundedRect(0, 0, self.width(), self.height(), 0, 0)
        else:
            #######################################################################################
            # full màn và cạnh tròn
            #######################################################################################
            path.addRoundedRect(0, 0, self.width(), self.height(), 10, 10)


        #######################################################################################
        # hiển thị viền app
        #######################################################################################
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillPath(path, QBrush(QColor(38, 49, 98)))
        painter.setPen(QColor(94,112,167))
        painter.drawPath(path)
    #######################################################################################

    #######################################################################################
    # hiệu ứng thông báo tin nhắn

    #######################################################################################
    # hiển thị ở góc màn hình ứng dụng
    def _on_resize(self, event):
        msg.move_notification()
        QMainWindow.resizeEvent(self, event)
    #######################################################################################
    # hiển thị 500 dòng dữ liệu 
    def ProcessingQThreadDataItemsCondition(self , data : dict):
        #######################################################################################
        # xử lý 500 dữ liệu và hiển thị với QThread
        self.thread = DataGenerator(self.total_items, self.batch_size, self.current_batch , data)
        self.thread.data_signal.connect(self.SubjectShowLoadData)
        self.thread.start()

        #######################################################################################
        # thông báo hiển thị

    def ProcessConfigSetting(self):

        processConfig = ConfigUser(widgets)
        if processConfig:
            msg.SendMsg(("Cập nhật thành công !",1))
        else:
            msg.SendMsg(("Không thể cập nhật !",0))
    #######################################################################################
    # thêm dữ liệu từ mảng vào bảng
    # [{}...]
    def SubjectShowLoadData(self, data):

        #######################################################################################
        # Vô hiệu hóa chế độ chọn và thiết lập chế độ chọn theo hàng
        # Tắt Selection các dòng trong Qtable
        #######################################################################################
        widgets.TableManage.setSelectionMode(QTableWidget.NoSelection)
        widgets.TableManage.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Xác định chỉ số cột cho 'message' và 'c_user'
        message_column_index = index_name.get("message", -1)
        c_user_column_index = index_name.get("c_user", -1)

        #######################################################################################
        # Thiết lập delegate cho cột 'message' và 'c_user'
        if message_column_index != -1:

            widgets.TableManage.setItemDelegateForColumn(message_column_index, RoundedBorderDelegate(self,color=QColor(70, 200, 245), bold=1))

        if c_user_column_index != -1:
            widgets.TableManage.setItemDelegateForColumn(c_user_column_index, RoundedBorderDelegate(self,color=QColor(0, 204, 204), bold=1))

        # END
        #######################################################################################
        # Thêm dữ liệu vào bảng

        for row_data in data:
            try:


                #######################################################################################
                # Lấy vị trí hàng hiện tại và chèn hàng mới
                #######################################################################################
                row_position = widgets.TableManage.rowCount()
                widgets.TableManage.insertRow(row_position)


                #######################################################################################
                # Thêm item checkbox vào cột đầu tiên
                #######################################################################################
                widgets.TableManage.setItem(row_position, 0, QTableTools.CheckboxNew(self))

                #######################################################################################
                # Thêm item số hàng vào cột thứ hai
                #######################################################################################
                item_count = QTableTools.SubjectItemsText(
                    self, text=str(row_position + 1), color=QColor(255,255,255), size_font=8)
                widgets.TableManage.setItem(row_position, 1, item_count)


                #######################################################################################
                # Thiết lập chiều cao hàng
                #######################################################################################
                widgets.TableManage.setRowHeight(row_position, 40)


                #######################################################################################
                # Thêm các item dữ liệu vào các cột tương ứng
                #######################################################################################
                for temp_name, value in row_data.items():
                    try:

                        #######################################################################################
                        # Xác định màu sắc dựa trên tên cột
                        #######################################################################################
                        color = QColor(20, 57, 39)  # Màu mặc định
                        if temp_name == "message":
                            value = time_lastest(value)
                            color = QColor(255,255,255)
                        elif temp_name == "c_user":
                            color = QColor(92, 0, 230)
                        else:
                            color =  QColor(255,255,255)


                        # END
                        #######################################################################################

                        #######################################################################################
                        # Tạo item với màu sắc và kích thước font đã chỉ định
                        #######################################################################################
                        if temp_name == "work":
                            typeAccount = widgets.ComboBoxTypeAccount.currentText().lower()
                            value = str(len(json.loads(open("./models/json/config.json","r",encoding="utf-8").read())["account.work"][typeAccount])) + " Actions !"
                        elif temp_name == "proxy":
                            value = "Local IP"
                        item_category = QTableTools.SubjectItemsText(
                            self, text=value, color=color, size_font=8)
                        
                        # Thêm item vào bảng ở vị trí hàng và cột tương ứng
                        if temp_name == "status":
                            if value == "Unknown":
                                color =  QColor(64, 191, 128)
                                item_category.setIcon(QIcon(r".\icons\png\icons8-dot-24.png"))
                            elif value == "LIVE":
                                item_category.setIcon(QIcon(r".\icons\png\icons8-dot-24_live.png"))
                                color =  QColor(64, 191, 128)
                        elif temp_name == "work":
                            item_category.setIcon(QIcon(r".\icons\png\icons8-thunder-24.png"))
                        widgets.TableManage.setItem(row_position, index_name[temp_name], item_category)

                    except KeyError:
                        # Bỏ qua nếu không tìm thấy chỉ số cột
                        continue

            except Exception as e:
                # In ra thông báo lỗi nếu có
                print(f"Error adding row data: {e}")
        #######################################################################################
        # Tăng giá trị biến đếm batch hiện tại
        # giá trị này tính số lượng số trang đã load 
        # {page} =  current_bacth * total_show 
        #######################################################################################
        self.current_batch += 1


        #######################################################################################        
        # thêm hiệu ứng selection line
        #######################################################################################
        QTableTools.AddSelectionItems(self , widgets)
    

    #######################################################################################/
    # check cuộn xuống 100 dòng sẽ load thêm
    
    def SubjectAutoLoadData(self):
        scrollbar = widgets.TableManage.verticalScrollBar()
        scrollbar.valueChanged.connect(lambda :QTableTools.HandleScroll(self,scrollbar,DataFillProcess))
        header = widgets.TableManage.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

    #######################################################################################
    # search trực tiếp trên TableWidget , chưa xử lý nhiều
    # Bug : search quá nhanh sẽ đơ app và lỗi isrunning chưa xử lý gì thêm / code : 191
    #######################################################################################
    def search(self):
         # Kiểm tra nếu thời gian từ lần tìm kiếm trước đó ít hơn 500ms
        if self.lastSearchTime.elapsed() < 500:
            print("time searh limit")
            return  # Không thực hiện tìm kiếm nếu chưa đủ thời gian chờ
        
        try:
            self.processingSearch = Search(widgets,widgets.line_search.text().lower())
            self.startprocessingSearch()
        except Exception as KeyError:
            print(KeyError)
        self.lastSearchTime.restart() # reset lại time đếm
    

    #######################################################################################
    # 2 hàm này hạn chế Bug / 191
    def startprocessingSearch(self):
        if not self.processingSearch.isRunning():
            self.processingSearch.start()
    def stopprocessingSearch(self):
        try:
            if self.processingSearch.isRunning():
                self.processingSearch.quit()
                self.processingSearch.wait()
        except Exception as KeyError:
            print(KeyError)
            return

    def closeEvent(self, event):
        self.stopprocessingSearch()
        event.accept()
    #######################################################################################



    #######################################################################################
    # Custom các frame
    def CustomShadowFrameApp(self):
        #######################################################################################
        # shadow effect frame_manage_tool , ... frame as 
        #######################################################################################
        Functions.ShadowFrameConditional(self , widgets.scrollArea_manage , QColor(1, 1, 1, 20))

        Functions.ShadowFrameConditional(self , widgets.frame_manage_main , QColor(1, 1, 1, 80))

        widgets.frame_manage_tool.setStyleSheet("QFrame{border-radius:10px;}")
        Functions.ShadowFrameConditional(self , widgets.frame_manage_tool , QColor(1, 1, 10, 50))

        widgets.frame_status_manage.setStyleSheet("QFrame{border-radius:10px;}")
        Functions.ShadowFrameConditional(self , widgets.frame_status_manage , QColor(1, 1, 10, 80))

        Functions.ShadowFrameConditional(self , widgets.frame_tool_two , QColor(0, 0, 10, 50))
    # END
    #######################################################################################



    
    #######################################################################################
    # phần này tạo icons khi di chuyển
    def EdgeGripShort(self):
        #######################################################################################
        # tạo icon kéo dãn khi di chuột gần mép
        self.left_grip = EdgeGrip(widgets.centralwidget, Qt.LeftEdge)
        self.right_grip = EdgeGrip(widgets.centralwidget, Qt.RightEdge)
        self.top_grip = EdgeGrip(widgets.centralwidget, Qt.TopEdge)
        self.bottom_grip = EdgeGrip(widgets.centralwidget, Qt.BottomEdge)
    

    #######################################################################################
    # mô phỏng kéo dài cho các cột
    #######################################################################################
    def InteractiveHeader(self):
        header = widgets.TableManage.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) # fix QThread destroyed is running
    #######################################################################################
    # Làm nét HD cho các hình ảnh trong APP
    #######################################################################################
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    #######################################################################################
    # Tự chỉnh checkbox trong QTable căn chính giữa
    #######################################################################################
    checkbox_style = CheckBoxStyle(app.style())

    #######################################################################################
    
    app.setWindowIcon(QIcon("./icons/logo/icons.png"))
    window = WindowInterface()
    sys.exit(app.exec_())




#######################################################################################
# BỊ CRUSH BƠ RÒI
#######################################################################################
'''

exec(text)