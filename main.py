import sys , os , ctypes , threading
from PyQt5.QtCore import QObject


# functions 
from models import * 
from widgets import *
widgets , resize  , processing_thread , msg  = None , None , None , None 

DataProcessingFill  , DataFillProcess = (None , None) , None
ThreadCheckbox = []
version = object

# index theo thứ tự bảng table

class WindowInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAutoFillBackground(True)
        # APPLY THE STYLESHEET
        self.setWindowFlag(Qt.FramelessWindowHint)
        


        # CALL ITEM * 
        global widgets , DataProcessingFill ,ThreadCheckbox, msg , index_name , DataFillProcess 
        
        self.is_left_mouse_pressed , self.first_selected_item = False , None
        self.ProxyQThread , self.DataThreadLoad = None ,None
        
        self.Thread ,self.ThreadBrowser_ , self.CheckButtonStart , self.checkmyaccount   = {} , None , True , None
        self.total_items, self.batch_size, self.current_batch = int(1e7) , 100 , 0

        


        
        # HIỂN THỊ TRONG CENTRALWIDGET CỦA APP
        widgets , msg = self.ui , Notification(self.ui.centralwidget)
        self.setWindowTitle("BeSyn - Quản Lý Đa Nền Tảng Tài Khoản")
        


        
        # TỰ ĐỘNG DỊCH CHUYỂN THANH THÔNG BÁO PHÙ HỢP KHI PHÓNG TO , THU NHỎ ỨNG DỤNG
        self.resizeEvent_ = self._on_resize
        
        # BUTTON LIST ARRAY

        self.buttons_ = ObjectTemp.TempsButtonTextWidgets(self , widgets)
        self.buttons_icons = ObjectTemp.TempsButtonIconsWidgets(self , widgets)
        
        
        self.buttons_tools = ObjectTemp.TempsButtonToolsWidgets(self , widgets)
            
        FrameRightClick(widgets,self)

        
        # THÊM NÚT CHO TABLE WIDGET
        widgets.TableManage.setHorizontalHeader(CustomHeaderHorizontal(widgets))
            
        
        """
            MOUSE RESIZE
        """
        self.RemoveWindowFlags()

        
        
        # SUBJECT CONNECT CÁC BUTTON
        self.SubjectConnectButton()
    
        
        # LOAD CÁC LỆNH VỀ UI_FUNCTIONS

        self.SubjectFunctions()


    

        
        # TẠO HEADERHORIZONTAL
        self.SubjectSetupTableManage()


        
        # TURN OFF FOCUS
        QTableTools.remove_focus(self, widgets.TableManage)

        # TỰ ĐỒNG TẠO DANH MỤC MẶC ĐỊNH VÀ LOAD ITEM LÊN COMBOBOX DANH MỤC
        self.SQLProcessing()

        
        

        
        # CUSTOMSCROLLBAR : THÊM HIỆU ỨNG THANH CUỘN CHO CÁC TABLEWIDGET
        widgets.TableManage.setVerticalScrollBar(CustomScrollBar(widgets.TableManage, Qt.Vertical))
        widgets.TableManage.setHorizontalScrollBar(CustomScrollBar(widgets.TableManage, Qt.Horizontal))



        
        # PHẦN NÀY TẠO BUTTON CÓ HÌNH ĐẠI DIỆN , THÊM HIỆU ỨNG ĐĂNG XUẤT , THÔNG TIN PROFILE TÓM TẮT
        self.MenuButtonProfileUser()


        
        # THÊM MODEL CHO TABLE WIDGET
        self.SubjectAutoLoadData()


        
        # MÔ PHỎNG CHẾ ĐỘ KÉO DÃN CHO CÁC CỘT
        self.InteractiveHeader()


        
        # TẠO ICONS HIỂN THỊ CON TRỎ KÉO DÃN MÀN HÌNH
        self.EdgeGripShort()
        
        # SEARCH
        self.lastSearchTime = QElapsedTimer()
        self.lastSearchTime.start()  # KHỞI ĐỘNG BỘ ĐẾM THỜI GIAN
        widgets.line_search.textChanged.connect(self.search)


        
        # LOAD DỮ LIỆU
        self.ComboboxFileActivedConnect()


        
        widgets.ComboboxFile.activated.connect(self.ComboboxFileActivedConnect)

        widgets.TableManage.selectionModel().selectionChanged.connect(self.MouseClickCheckBox)

        widgets.TableManage.cellClicked.connect(self.ShiftAutoCheckbox)

        widgets.TableManage.cellClicked.connect(self.CheckBoxCount)

        

        widgets.TableManage.cellDoubleClicked.connect(lambda row , column,widgets=widgets:QTableTools.CopyColumnContentDoubleClick(self , widgets , row , column))
        self.show()

        widgets.btn_category.clicked.connect(self.CustomFile)

        
        # END 
        



    def CustomFile(self):
        menu = CustomMenuFolder(widgets)
        widgets.btn_category.setMenu(menu)
        widgets.btn_category.showMenu()
        widgets.btn_category.setMenu(None)


    # LẤY CÁC UID ĐÃ CHECKED
    def GetAccountChecked(self):
        obj = []
        for i in range(widgets.TableManage.rowCount()):
            checkbox = widgets.TableManage.item(i, 0)
            if checkbox.checkState() == 2:
                c_user = widgets.TableManage.item(i, 2).text()
                obj.append(c_user)
        
        return obj
    def CheckBoxCount(self,row, column ):
        total = 0
        for i in range(widgets.TableManage.rowCount()):
            checkbox = widgets.TableManage.item(i, 0)
            if checkbox.checkState() == 2:
                total += 1
        
        if total == 0:
            self.ToolsHideButton()
        else:
            self.ToolsShowButton()
            widgets.btn_run.setText("RUN ({})".format(str(total)))
        
        widgets.label_select.setText(f"({str(total)})")
    
    # ĐỔI TRẠNG THÁI CHECKBOX KHI NGƯỜI DÙNG NHẤN SHIFT ĐỂ CHỌN CÁC DÒNG
    def ShiftAutoCheckbox(self, row, column ):
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            if self.first_selected_item is not None:
                first_row, first_col = self.first_selected_item
                widgets.TableManage.clearSelection()
                for r in range(min(first_row, row), max(first_row, row) + 1):
                    for c in range(min(first_col, column), max(first_col, column) + 1):
                        
                        # r : rows 
                        item = widgets.TableManage.item(r, 0)
                        
                        # set Checked
                        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                        item.setCheckState(Qt.Checked)
        else:
            self.first_selected_item = (row, column)

    
    # CLICK FRAME AUTO SET CHECKED
    def MouseClickCheckBox(self , index):

        for obj in index.indexes():
            if obj.column() == 0:
                item =widgets.TableManage.item(obj.row(), 0)
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                item.setCheckState(Qt.Checked)

    def SubjectFunctions(self):
        
        # TOGGLE CHECKED AUTO REFRESH
        # TOGGLE BUTTON TEXT , ICONS 

        # CHUYỂN ĐỔI CSS CHO CÁC NÚT Ở MENU
        Functions.SwitchButtonCssChecked(self ,self.buttons_) # BUTTON TEXT

        
        # các nút icons khi ẩn menu
        Functions.SwitchButtonToolsCssChecked(self ,self.buttons_icons) # BUTTON ICONS

        
        # CÁC NÚT TOOLS Ở HOME
        Functions.SwitchButtonToolsCssChecked(self ,self.buttons_tools)

        # Functions.ButtonPlaySound(self , self.buttons_tools)
        
        # XỬ LÝ TỰ ĐỔI TRẠNG THÁI KHI NGƯỜI DÙNG CLICK VÀO Ô FRAME CHỨA CHECKBOX
        Functions.AutoSwitchCheckboxStatus(self , widgets)

        
        # CUSTOMS CSS CHO BTN_PROFILE Ở TASK TOP
        # SOUND OPENING
        Functions.OpenSoundApp(self)

        Functions.ShadowFrameConditional(self, widgets.frame_taskbar,QColor(0,10,10,100))


    def SubjectUpdateProxy(self):
        self.ProxyQThread = ProxySQL()
        self.ProxyQThread.start()
    
    def SubjectSetupTableManage(self):
        QTableTools.SubjectNewHorizontalHeader(self , widgets)


        QTableTools.SubjectHiddenColumn(self , widgets)

        
        # GIỚI HẠN CHIỀU RỘNG CỦA CỘT
        QTableTools.SetColumnWidthTableWidget(self , widgets)


    # ẨN ICONS SEARCH , HIỆN FRAME SEARCH
    def ShowFrameSearch(self):
        widgets.frame_search.setMaximumSize(250,35)
        widgets.btn_search_icons.hide()
    def HideFrameSearch(self):
        widgets.line_search.clear()
        widgets.frame_search.setMaximumSize(0,35)
        widgets.btn_search_icons.show()
    # CHECK TÀI KHOẢN
    def CheckAccount(self):
        self.checkmyaccount = CheckFacebook(self.GetAccountChecked())
        self.checkmyaccount.signal.connect(self.BrowserUpdate)
        self.checkmyaccount.start()
    
# XÓA TÀI KHOẢN
    def show_confirmation(self):
        window_widgets , window_ui = Ui_Connect.show_ui(self , Ui_NotifiRemove)
        window_ui.show()
        window_widgets.btn_no.clicked.connect(lambda:window_ui.close())
        window_widgets.btn_yes.clicked.connect(lambda:window_ui.close())
        window_widgets.btn_yes.clicked.connect(self.RemoveAccount)
        window_widgets.btn_yes.clicked.connect(lambda: self.RemoveWindowFlags())
        window_widgets.btn_no.clicked.connect(lambda: self.RemoveWindowFlags())
    def RemoveAccount(self):

        itemRemove = []
        row = 0
        while row <= widgets.TableManage.rowCount():
            item = widgets.TableManage.item(row, 0)
            # Kiểm tra nếu item không phải là None trước khi gọi checkState()
            if item is not None and item.checkState() is not None and item.checkState() == 2:
                itemRemove.append(widgets.TableManage.item(row , 2).text())
                widgets.TableManage.removeRow(row)
            else:
                row += 1
    

        # self.ComboboxFileActivedConnect()
        print(itemRemove)


    # SUBJECT CONNECT CÁC BUTTON
    def SubjectConnectButton(self):
        
        # HIỂN THỊ DANH SÁCH FOLDER KHI NHẤN 

        widgets.btn_delete.clicked.connect(self.show_confirmation)

        widgets.btn_unchecked.clicked.connect(lambda:QTableTools.UnCheckbox(self , widgets))
        widgets.btn_unchecked.clicked.connect(self.ToolsHideButton)

        widgets.btn_CheckAccount.clicked.connect(self.CheckAccount)

        widgets.btn_search_icons.clicked.connect(self.ShowFrameSearch)
        widgets.btn_search_hide.clicked.connect(self.HideFrameSearch)

        # ẨN CÁC NÚT
        self.ToolsHideButton()

        widgets.ComboboxFile.setStyle(NoFocusProxyStyle(widgets.ComboboxFile.style()))

        Functions.ShadowFrameConditional(self,widgets.SettingPage,QColor(0,10,10,100))
        
        FrameID =  [widgets.FrameID_ProfileLog , widgets.FrameID_AutoSortSize,
                    widgets.FrameID_Backup,widgets.FrameID_BrowserOptimization,
                    widgets.FrameID_Proxy1,widgets.FrameID_Proxy2,widgets.FrameID_ContentChatGpt,
                    widgets.FrameID_ChromeHeadless]
        Functions.AnimatedToggleButton(self , FrameID)
        
        widgets.btn_hide.clicked.connect(lambda: Functions.AnimationSwitchMenu(self, widgets))
        widgets.btn_hide_icons.clicked.connect(lambda: Functions.AnimationSwitchMenu(self, widgets))
        

        
        widgets.btn_maximum.clicked.connect(lambda: Functions.ResizeMode(self, widgets))
        widgets.btn_minimum.clicked.connect(lambda: self.showMinimized())

        widgets.btn_close.clicked.connect(lambda: self.close())

        
        # FUNCTIONS BUTTON CLICKED CONNECT

        widgets.btn_add.clicked.connect(self.window_additem)
        widgets.btn_proxy.clicked.connect(self.window_proxies)

        
        # LOAD LẠI DỮ LIỆU
        widgets.btn_refresh.clicked.connect(self.ComboboxFileActivedConnect)

        
        # CÀI DẶT KỊCH BẢN
        widgets.btn_plan_tool.clicked.connect(self.WidgetFrameScheme)
        widgets.btn_plan_tool_icons.clicked.connect(self.WidgetFrameScheme)


        widgets.btn_all.clicked.connect(self.SwapWidgetFrameHome)
        widgets.btn_all_icons.clicked.connect(self.SwapWidgetFrameHome)


        # CÀI ĐẶT CHUNG
        widgets.btn_setting.clicked.connect(self.WidgetFrameSetting)
        widgets.btn_setting_icons.clicked.connect(self.WidgetFrameSetting)

        # CHUYỂN ĐỔI BACK GIỮA CÁC FRAME
        self.SwapWidgetFrameHome()
        widgets.btn_back.clicked.connect(self.SwapWidgetFrameHome)
        widgets.btn_back_2.clicked.connect(self.SwapWidgetFrameHome)

        
        # LƯU CÀI ĐẶT VÀ HIỂN YHIJ THÔNG BÁO THÀNH CÔNG
        widgets.btn_settingSave.clicked.connect(self.ProcessConfigSetting)
        widgets.btn_settingSave.clicked.connect(self.SubjectUpdateProxy)
        # CHẠY
        widgets.btn_run.clicked.connect(self.startRun)
        widgets.btn_stop.clicked.connect(self.stopRun)
    


    def emitThreadStop(self,infoID):
        try:
            ThreadCheckbox.remove(infoID)
        finally:
            return
    def BrowserThreadStop(self):

        self.ThreadBrowser_ = BrowserKill({'Thread':self.Thread,'ThreadCheckbox':ThreadCheckbox})
        if not self.ThreadBrowser_.isRunning():
            self.ThreadBrowser_.signal.connect(self.emitThreadStop)
            self.ThreadBrowser_.start()
    def stopRun(self):
        self.KillBrowserBeta()
        self.BrowserThreadStop() # OUT THREAD
    def startRun(self):
        
        self.timerStart = []  # LƯU TRỮ CÁC TIMER
        self.width_sort , self.height_sort , self.y_position = 350 , 400 , 0

        # DANH SÁCH CÁC UID ĐÃ CHỌN
        for i in range(widgets.TableManage.rowCount()):
            checkbox = widgets.TableManage.item(i, 0)
            if checkbox.checkState() == 2:
                ThreadCheckbox.append(widgets.TableManage.item(i, 2).text())

        self.timerIndex = 0  # KHỞI TẠO CHỈ SỐ ĐỂ THEO DÕI

        # NẾU CÓ ITEM ĐƯỢC CHỌN, BẮT ĐẦU CHẠY TIMER
        if ThreadCheckbox:
            self.timer = QTimer()
            self.timer.timeout.connect(self.runNextThread)
            self.timer.start(1000)  # CHẠY MỖI 1 GIÂY
        
        self.CheckButtonStart = False
    def runNextThread(self):
        if self.timerIndex < len(ThreadCheckbox):
            infoID = ThreadCheckbox[self.timerIndex]
            self.RunBroswerThread(self.timerIndex, infoID)
            self.timerIndex += 1
        else:
            self.timer.stop()  # DỪNG TIMER KHI ĐÃ CHẠY HẾT CÁC HÀM
    


    def BrowserUpdate(self,obj):

        infoID = obj['uid']
        if obj['code'] is not 99:
            obj['msg'] = keys[obj['code']]

        for row in range(widgets.TableManage.rowCount()):
            if widgets.TableManage.item(row , 2).text() == infoID:
                obj.update({'row':row})
                # CẬP NHẬT TÌNH TRẠNG TÀI KHOẢN
                if obj['code'] == 828281030927956:
                    QTableTools.ChangeAccount(self , widgets , obj , 0)
                elif obj['code'] == 200:
                    QTableTools.ChangeAccount(self , widgets , obj , 1)
                elif obj['code'] == 300:
                    QTableTools.ChangeAccount(self , widgets , obj , 0)
                elif obj['code'] == 20032006:
                    SQL(obj["SQL"]).SQLUpdateDataFromKey(obj)
                # HIỂN THỊ MSG LÊN DỮ LIỆU
                color =  QColor(255,255,255)
                item_category = QTableTools.SubjectItemsText(
                            self, text=str(obj['msg']), color=color, size_font=8)
                widgets.TableManage.setItem(row, 14, item_category)
                return
    def RunBroswerThread(self,number,infoID):

        # get wight , height 
        user32 = ctypes.windll.user32
        width = user32.GetSystemMetrics(0)  # CHIỀU RỘNG CỦA MÀN HÌNH
        height = user32.GetSystemMetrics(1)  # CHIỀU CAO CỦA MÀN HÌNH

        max_width =  int(width / 350)
        max_height =  int(height / 400) - 1
        
        x_position = (number % max_width) * self.width_sort
        if (number % max_width) == 0 and number != 0:
            self.y_position += (self.height_sort + 10)
        obj = {'number':number,'uid':infoID,'x_position':x_position,'y_position':self.y_position}

        self.Thread[infoID] = Browser(obj)
        self.Thread[infoID].signal.connect(self.BrowserUpdate)
        self.Thread[infoID].start()
    # CHUYỂN ĐỔI FRAME MÀN HÌNH CỦA STACK WIDGET
    


    def SwapWidgetFrameHome(self):
        widgets.stackedWidget.setCurrentWidget(widgets.HomePage)
    


    
    # MÀN HÌNH KỊCH BẢN
    def WidgetFrameScheme(self):
        widgets.stackedWidget.setCurrentWidget(widgets.PlanPage)

        SubjectQList.ShowCardItems(self , widgets)



    
    # MÀN HÌNH CÀI ĐẶT CHUNG
    def WidgetFrameSetting(self):
        ShowConfig().Config(widgets)
        widgets.stackedWidget.setCurrentWidget(widgets.SettingPage)



    
    # XÓA THANH TIÊU ĐỀ VÀ XỬ LÝ DI CHUYỂN
    def RemoveWindowFlags(self):

        
        # MÀU NỀN CỦA GIAO DIỆN CHÍNH VỀ BAN ĐẦU
        

        self.setAttribute(Qt.WA_TranslucentBackground) 

        
        # XỬ LÝ DI CHUYỂN ỨNG DỤNG
        self.resize = Resize(self)



    
    # TỰ ĐỒNG TẠO DANH MỤC MẶC ĐỊNH VÀ LOAD ITEM LÊN COMBOBOX DANH MỤC
    def SQLProcessing(self):
        
        # SQL
        # TẠO THƯ MỤC MẶC ĐỊNH
        SubjectSQL.CreateTableNew(self, name= "ALL",widgets=widgets)

        
        SubjectProcessFile.LoadNameTabelSQL(self , widgets)        

        
    

    
    # PHẦN NÀY TẠO BUTTON CÓ HÌNH ĐẠI DIỆN , THÊM HIỆU ỨNG ĐĂNG XUẤT , THÔNG TIN PROFILE TÓM TẮT

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

    
    

    # CĂN CHỈNH MÀN HÌNH PHỤ Ở CHÍNH GIỮA GIAO DIỆN APP
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

    
    # MÀN HÌNH THÊM DỮ LIỆU
    def window_additem(self):
        # code sql/300
        
        self.start_blur()
        Namecategory =  widgets.ComboboxFile.currentText()
        NameaccountType =  'Facebook'
        # NameaccountType =  widgets.ComboBoxTypeAccount.currentText()


        
        # CALL FUNCTIONS CONNECT UI
        # CHỨC NĂNG HIỂN THỊ GUI THÊM DỮ LIỆU TÀI KHOẢN
        # CALL SUB FROM FUNCTIONS SHOW UI CLONE
        window_widgets , windows_ui = Ui_Connect.show_ui(self, Ui_TabWidget)
        window_widgets.tabWidget.removeTab(1)
        window_widgets.tabWidget.setCurrentIndex(0)

        
        # căn giữa
        self.center(windows_ui)

        
        # TOGGLE FRAME, BUTTON TO SHADOW
        # CHỈNH SỬA LÀM BÓNG CÁC FRAME

        


        
        # XỬ LÝ THAO TÁC CLICK BUTTON TRONG GIAO DIỆN CHÍNH
        self.SubjectDataProcessingQThread = SubjectDataProcessing(window_widgets)
        self.SubjectDataProcessingQThread.signal.connect(self.signalSubjectDataProcessing)
        window_widgets.plain_item.textChanged.connect(self.startSubjectDataProcessing)

        window_widgets.item_add.clicked.connect(lambda : self.SubjectDataProcessingConfirm(window_widgets , windows_ui))
        window_widgets.item_add.clicked.connect(lambda : self.reset_blur())
        window_widgets.item_close.clicked.connect(lambda : windows_ui.close())
        window_widgets.item_close.clicked.connect(lambda : self.reset_blur())
        window_widgets.item_close.clicked.connect(lambda: self.RemoveWindowFlags())

        # Thêm Text và Xóa để hiện Placehoder
        window_widgets.plain_item.setPlaceholderText("Nhập tài khoản ...")
        window_widgets.plain_item.setPlainText("...")
        window_widgets.plain_item.clear()
        
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

    
    # chạy QThread xử lý định dạng dữ liệu và gán cho DataProcessingFill
    def startSubjectDataProcessing(self):
        if not self.SubjectDataProcessingQThread.isRunning():
            self.SubjectDataProcessingQThread.start()
    def signalSubjectDataProcessing(self , data : tuple):
        global DataProcessingFill 
        DataProcessingFill = data

    
    # phần này xử lý dữ liệu nhập , dùng QThread tránh GUI Lag
    def SubjectDataProcessingConfirm(self , window_widgets , window_ui):
        global DataProcessingFill , processing_thread
        
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
        
        
        # xử lý dữ liệu và gửi tới hàm on_processing
        
        processing_thread = ProcessingThread(window_widgets , DataProcessingFill , textCurrent)

        
        # truyền dữ liệu tới OnProcessingFinished() khi hoàn thành xong task và show lên table
        processing_thread.processing_finished.connect(self.OnProcessingDataFinished)
        processing_thread.start()

        
        # đòng cửa sổ nhập
        window_ui.close()


    
    # xóa các dữ liệu hiển thị và thêm dữ liệu ở mục chỉ định
    def ComboboxFileActivedConnect(self):
        global DataFillProcess
        
        widgets.TableManage.clear()
        
        # Config lại headerhorizontal 
        self.SubjectSetupTableManage()
        self.total_items, self.batch_size, self.current_batch = int(1e7) , 100 , 0
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

    
    
    # Dữ liệu ở hàm SubjectDataProcessingConfirm() chạy QThread xong sẽ truyền tới hàm này
    
    def OnProcessingDataFinished(self , res : dict, widgets_ : object):
        global DataFillProcess
        
        # gán dữ liệu đã xử lý để gửi tới hàm thêm dữ liệu
        DataFillProcess = res
        self.maxTotal =  len(DataFillProcess)
        Functions.UpdateLabelTotalAccount(self , widgets , len(DataFillProcess))
        
        # insert dữ liệu vào table
        self.SubjectOnProcessinginsertDataFinished = SubjectOnProcessingDataFinished(widgets, self.NameCategory , DataFillProcess)
        self.startOnProcessingDataFinished()
        
        # lấy 500 dữ liệu đầu tiên và hiển thị , tránh lag gui
        # self._GetDataThread = GetDataThread(widgets, self.NameCategory , self.maxTotal)
        # self._GetDataThread.signal.connect(self.signalOnProcessingDataFinished)
        # self.starGetDataThread()

        msg.SendMsg(("Load dữ liệu có thể mất chút thời gian !!!",1))

                                #       , Ui_main , [{},{} ...]      , ["","" ...]

    
    # lấy dữ liệu xử lý định dạng phù hợp để truyền tới add item vào QTabel
    
    def signalOnProcessingDataFinished(self , data : list):
        global DataFillProcess 
        DataFillProcess = data
        # self.ProcessingQThreadDataItemsCondition(DataFillProcess)
        self.ComboboxFileActivedConnect()
        
        # cập nhật thông số tài khoản

        if len(DataFillProcess) == self.maxTotal:
            msg.SendMsg(("Thêm thành công !",                1))
        else:
            msg.SendMsg(("Đang load dữ liệu !",                1))

    
    # QThread tránh lỗi isrunning
    
    def starGetDataThread(self):
        if not self._GetDataThread.isRunning():
            self._GetDataThread.start()

    def startOnProcessingDataFinished(self):
        if not self.SubjectOnProcessinginsertDataFinished.isRunning():
            self.SubjectOnProcessinginsertDataFinished.start()

    
    # Gui hiển thị dữ liệu nhập Proxy . dùng Tabwidget và chuyển đổi sang index : 1
    
    def window_proxies(self):
        
        self.start_blur()
        window_widgets , windows_ui = Ui_Connect.show_ui(self, Ui_TabWidget)
        window_widgets.tabWidget.removeTab(0)
        window_widgets.tabWidget.setCurrentIndex(1)
        self.center(windows_ui)


        # widgets.tabWidget.widget(0).hide()
        # window_widgets -> Object : sử dụng để gọi các frame , button ...
        # window_ui      -> OBject : sử dụng để close , show , công dụng như hàm self.show()
        # Call Functions Connect UI
        self.item_CheckProxy_Change  =  False 
        
        # Call Sub from Functions Show UI Clone PROXIES
        # window_widgets.item_add.clicked.connect(lambda : self.SubjectDataProcessingConfirm(window_widgets , windows_ui))
        window_widgets.item_closeProxy.clicked.connect(lambda : windows_ui.close())
        window_widgets.item_closeProxy.clicked.connect(lambda: self.RemoveWindowFlags())

        window_widgets.item_closeProxy.clicked.connect(lambda : self.reset_blur())
        window_widgets.item_import.clicked.connect(lambda : self.reset_blur())
        
        # hiện holder

        window_widgets.plain_Proxy.setPlaceholderText("Nhập Proxy ...")
        window_widgets.plain_Proxy.setPlainText("...")
        window_widgets.plain_Proxy.clear()


        # cập nhật proxy và thêm
        window_widgets.item_import.clicked.connect(lambda:self.ProxyAdd(windows_ui))

        window_widgets.plain_Proxy.textChanged.connect(lambda: self.ProxyPlainCount(window_widgets))
        window_widgets.item_ClearProxy.clicked.connect(lambda: self.ProxyClear(window_widgets))

        proxy_list = json.loads(open(your_dir_config,"r",encoding="utf-8").read())["proxy"]["list"]
        proxy_text = "\n".join(proxy_list) if isinstance(proxy_list, list) else proxy_list
        window_widgets.plain_Proxy.setPlainText(proxy_text)
        
        # run , check script

    def ProxyClear(self , window_widgets):
        window_widgets.label_5.setText(str())
        window_widgets.plain_Proxy.clear()

        # Cập nhật và Xóa Proxy
        ConfigProxy().ProxyClear()
        


    def ProxyPlainCount(self, window_widgets):
        self.proxyPlainText = [prx.strip("\n") for prx in window_widgets.plain_Proxy.toPlainText().split("\n")]

        window_widgets.label_5.setText("Tổng : {}".format(len(self.proxyPlainText)))
    def ProxyAdd(self , windows_ui):


        # Cập nhật và lưu Proxy mới
        ConfigProxy().ProxyAdd(self.proxyPlainText)
        

        windows_ui.close()
        self.RemoveWindowFlags()
        if self.proxyPlainText != "":
            msg.SendMsg(("Thêm Proxy Thành Công !",1))

    
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

    
    
    # hiệu ứng làm tròn viền
    # def paintEvent(self, event):
    #     painter = QPainter(widgets.frame_main)
    #     path = QPainterPath()
    #     if self.isMaximized():
    #         
    #         # full màn và cạnh nhọn
    #         
    #         path.addRoundedRect(0,0, self.width() , self.height() , 0, 0)

    #     else:
    #         
    #         # cạnh tròn
    #         
    #         path.addRoundedRect(0,0, self.width() , self.height(), 10, 10)


    #     
    #     # hiển thị viền app
    #     
    #     painter.setRenderHint(QPainter.Antialiasing, True)
    #     painter.fillPath(path, QBrush(QColor(38, 49, 98)))
    #     painter.setPen(QColor(94,112,167))
    #     painter.drawPath(path)
    

    
    # HIỆU ỨNG LÀM MỜ
    def start_blur(self):
        self.ModeEffect = QGraphicsBlurEffect()
        self.ModeEffect.setBlurRadius(3)  # Độ mờ của hiệu ứng
        widgets.frame_main.setGraphicsEffect(self.ModeEffect)  # Áp dụng hiệu ứng mờ

    def reset_blur(self):
        widgets.frame_main.setGraphicsEffect(None)  # Gỡ bỏ hiệu ứng mờ
    
    # hiển thị ở góc màn hình ứng dụng
    def _on_resize(self, event):
        msg.move_notification()
        QMainWindow.resizeEvent(self, event)
    
    # hiển thị 500 dòng dữ liệu 
    def ProcessingQThreadDataItemsCondition(self , data : dict):
        
        # xử lý 500 dữ liệu và hiển thị với QThread
        self.thread = DataGenerator(self.total_items, self.batch_size, self.current_batch , data)
        self.thread.data_signal.connect(self.SubjectShowLoadData)
        self.thread.start()

        
        # thông báo hiển thị

    def ProcessConfigSetting(self):

        processConfig = ConfigUser(widgets)
        if processConfig:
            msg.SendMsg(("Cập nhật thành công !",1))
        else:
            msg.SendMsg(("Không thể cập nhật !",0))
    
    # thêm dữ liệu từ mảng vào bảng
    # [{}...]
    def SubjectShowLoadData(self, data):

        
        # Vô hiệu hóa chế độ chọn và thiết lập chế độ chọn theo hàng
        # Tắt Selection các dòng trong Qtable
        
        
        self.DataThreadLoad = LoadNewData(widgets,data)

        if not self.DataThreadLoad.isRunning():
            self.DataThreadLoad.start()
        
        # Tăng giá trị biến đếm batch hiện tại
        # giá trị này tính số lượng số trang đã load 
        # {page} =  current_bacth * total_show 
        
        self.current_batch += 1


                
        # thêm hiệu ứng selection line
        
        QTableTools.AddSelectionItems(self , widgets)
    

    
    def ToolsHideButton(self):
        listButton  = [widgets.btn_run , widgets.btn_stop, widgets.btn_delete ,\
                        widgets.btn_CheckAccount,widgets.btn_export\
                            ,widgets.btn_killBrowser,widgets.btn_unchecked,\
                                widgets.btn_CheckProxy]

        for btn in listButton:
            btn.hide()
    def ToolsShowButton(self):
        listButton  = [widgets.btn_run , widgets.btn_stop, widgets.btn_delete ,\
                        widgets.btn_CheckAccount,widgets.btn_export\
                            ,widgets.btn_killBrowser,widgets.btn_unchecked\
                            ,widgets.btn_CheckProxy]

        for btn in listButton:
            btn.show()
    # CHECK CUỘN XUỐNG 100 DÒNG SẼ LOAD THÊM
    def SubjectAutoLoadData(self):
        scrollbar = widgets.TableManage.verticalScrollBar()
        scrollbar.valueChanged.connect(lambda :QTableTools.HandleScroll(self,scrollbar,DataFillProcess))
        header = widgets.TableManage.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

    
    # search trực tiếp trên TableWidget , chưa xử lý nhiều
    # Bug : search quá nhanh sẽ đơ app và lỗi isrunning chưa xử lý gì thêm / code : 191
    
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
    


    

    


    
    # Custom các frame
    def CustomShadowFrameApp(self):
        
        # shadow effect frame_manage_tool , ... frame as 
        
        Functions.ShadowFrameConditional(self , widgets.scrollArea_manage , QColor(1, 1, 1, 20))

        Functions.ShadowFrameConditional(self , widgets.frame_manage_main , QColor(1, 1, 1, 80))

        widgets.frame_manage_tool.setStyleSheet("QFrame{border-radius:10px;}")
        Functions.ShadowFrameConditional(self , widgets.frame_manage_tool , QColor(1, 1, 10, 50))

        widgets.frame_status_manage.setStyleSheet("QFrame{border-radius:10px;}")
        Functions.ShadowFrameConditional(self , widgets.frame_status_manage , QColor(1, 1, 10, 80))

        Functions.ShadowFrameConditional(self , widgets.frame_tool_two , QColor(0, 0, 10, 50))
    # END
    


    # Đóng Browser

    def ThreadBrowser_BrowserBeta(self):
        for proc in process_iter(['pid', 'name']):
            try:
                # Nếu tên tiến trình là 'chrome.exe' (Windows) hoặc 'chrome' (macOS/Linux)
                if proc.info['name'] in ('Chrome.exe', 'chrome'):
                    proc.terminate()  # Gửi tín hiệu kết thúc
                    proc.wait()       # Chờ tiến trình kết thúc
            except:
                pass
    def KillBrowserBeta(self):
        threading.Thread(target=(self.ThreadBrowser_BrowserBeta),args=()).start()
    ####
    # phần này tạo icons khi di chuyển
    def EdgeGripShort(self):
        
        # tạo icon kéo dãn khi di chuột gần mép
        self.left_grip = EdgeGrip(widgets.centralwidget, Qt.LeftEdge)
        self.right_grip = EdgeGrip(widgets.centralwidget, Qt.RightEdge)
        self.top_grip = EdgeGrip(widgets.centralwidget, Qt.TopEdge)
        self.bottom_grip = EdgeGrip(widgets.centralwidget, Qt.BottomEdge)
    

    
    # mô phỏng kéo dài cho các cột
    
    def InteractiveHeader(self):
        header = widgets.TableManage.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)


class BrowserKill(QThread):
    signal = pyqtSignal(object)
    def __init__(self, obj):
        super(BrowserKill,self).__init__()

        self.Thread = obj['Thread']
        self.ThreadCheckbox =  obj['ThreadCheckbox']
    
    def close(self,infoID):
        self.Thread[infoID].stop()
        self.signal.emit(infoID)
    def run(self):

        for infoID in self.ThreadCheckbox:
            threading.Thread(target=(self.close),args=(infoID,)).start()


    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) # fix QThread destroyed is running
    
    # Làm nét HD cho các hình ảnh trong APP
    
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    
    # Tự chỉnh checkbox trong QTable căn chính giữa
    
    checkbox_style = CheckBoxStyle(app.style())

    
    
    app.setWindowIcon(QIcon("./icons/logo/icons.png"))

    window = WindowInterface()
    sys.exit(app.exec_())





# BỊ CRUSH BƠ RÒI
