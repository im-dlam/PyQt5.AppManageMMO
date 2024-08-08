import sys

# ///////////////////////////
# functions 
from models import * 
from widgets import *
widgets , resize  , processing_thread , msg  = None , None , None , None 

DataProcessingFill  , DataFillProcess = (None , None) , None

version = object
# ///////////////////////////////////
# index theo thứ tự bảng table

class WindowInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # //////////////////////////////////
        # call item * 
        global widgets , DataProcessingFill , msg , index_name , DataFillProcess 
        # //////////////////////////////////

        self.first_selected_item =  None 
        self.total_items, self.batch_size, self.current_batch = int(1e7) , 1000 , 0

        # ///////////////////////////////////////


        # ///////////////////////////////
                                                # Hiển thị trong centralwidget của app
        self.setMinimumSize(QtCore.QSize(1270, 0))
        widgets , msg = self.ui , Notification(self.ui.centralwidget)

        self.setWindowTitle("BetaLogin - Quản Lý Đa Nền Tảng Tài Khoản")
        # ///////////////////////////////////////


        # //////////////////////////////////////
        # Tự động dịch chuyển thanh thông báo phù hợp khi phóng to , thu nhỏ ứng dụng
        self.resizeEvent_ = self._on_resize
        # /////////////////////////////////////////////////////////////
        # button list array

        self.buttons_ = ObjectTemp.TempsButtonTextWidgets(self , widgets)
        self.buttons_icons = ObjectTemp.TempsButtonIconsWidgets(self , widgets)
        
        # //////////////////////////////////
        self.buttons_tools = ObjectTemp.TempsButtonToolsWidgets(self , widgets)
            
        FrameRightClick(widgets,self)

        # //////////////////////////
        # thêm nút cho table widget
        widgets.TableManage.setHorizontalHeader(CustomHeaderHorizontal(self))
            
        # //////////////////////////////////////////////////////////////
        """
            Mouse resize
        """
        self.RemoveWindowFlags()

        # //////////////////////////////////////////////////////////////
        # Replace central widget with the custom one
        # widgets.centralwidget.setStyleSheet(central_script.format(10))
        
        # Subject connect các button
        self.SubjectConnectButton()

        # /////////////////////////
        # Load các lệnh về Ui_Functions

        self.SubjectFunctions()



        # //////////////////////////////////////////////////////////
        # custom shadow frame

        # ////////////////////////////////////////////////////////

        self.SubjectSetupTableManage()
        # ///////////////////////////////////////////////////////
        # turn off focus
        QTableTools.remove_focus(self, widgets.TableManage)

        # Tự đồng tạo danh mục mặc định và load item lên combobox danh mục
        self.SQLProcessing()

        # ////////////////////////////////////////////
        # Tạo cột tiêu đề nằm ngang | 14 cột
        

        # ///////////////////////////////////////////////////////////
        # custom scroll TableManage
        # widgets.TableManage.setHorizontalHeaderItem()
        # CustomScrollBar : thêm hiệu ứng thanh cuộn cho các tablewidget
        widgets.TableManage.setVerticalScrollBar(CustomScrollBar(widgets.TableManage, Qt.Vertical))
        widgets.TableManage.setHorizontalScrollBar(CustomScrollBar(widgets.TableManage, Qt.Horizontal))



        # //////////////////////////////////////////////////////////
        # phần này tạo button có hình đại diện , thêm hiệu ứng đăng xuất , thông tin profile tóm tắt
        self.MenuButtonProfileUser()

        # //////////////////////////////////
        # thêm model cho table widget
        self.SubjectAutoLoadData()
        # //////////////////////////////
        # mô phỏng chế độ kéo dãn cho các cột
        self.InteractiveHeader()
        # //////////////////////////////

        self.EdgeGripShort()
        # ///////////////////////
        # search

        widgets.line_search.textChanged.connect(self.search)

        # /////////////////////////////
        # Load dữ liệu
        self.ComboboxFileActivedConnect()
        widgets.ComboboxFile.activated.connect(self.ComboboxFileActivedConnect)

        widgets.TableManage.selectionModel().selectionChanged.connect(self.MouseClickCheckBox)

        widgets.TableManage.cellClicked.connect(self.OnCellClickCheckBox)
        self.show()












    # //////////////////////////
    # đổi trạng thái checkbox khi người dùng nhấn SHIFT để chọn các dòng

    def OnCellClickCheckBox(self, row, column):
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            print(row , column)
            if self.first_selected_item is not None:
                first_row, first_col = self.first_selected_item
                widgets.TableManage.clearSelection()
                for r in range(min(first_row, row), max(first_row, row) + 1):
                    for c in range(min(first_col, column), max(first_col, column) + 1):
                        # ///////////////
                        # r : rows 
                        print("OK")
                        item = widgets.TableManage.item(r, 0)
                        # //////////////////
                        # set Checked
                        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                        item.setCheckState(Qt.Checked)
        else:
            self.first_selected_item = (row, column)

    # ///////////////////////////////
    # click frame auto set checked
    def MouseClickCheckBox(self , index):

        for obj in index.indexes():
            if obj.column() == 0:
                item =widgets.TableManage.item(obj.row(), 0)
                item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                item.setCheckState(Qt.Checked)

    def SubjectFunctions(self):
        # //////////////////////////////////////////////////////////
        # toggle checked auto refresh
        # toggle button text , icons 

        # chuyển đổi css cho các nút ở menu
        Functions.SwitchButtonCssChecked(self ,self.buttons_) # button text

        # //////////////////////////////////
        # các nút icons khi ẩn menu
        Functions.SwitchButtonToolsCssChecked(self ,self.buttons_icons) # button icons

        # /////////////////////////////////////////////////////
        # các nút tools ở home
        Functions.SwitchButtonToolsCssChecked(self ,self.buttons_tools)

        Functions.ButtonPlaySound(self , self.buttons_tools)
        # //////////////////////////////////////////////////
        # xử lý tự đổi trạng thái khi người dùng click vào ô frame chứa checkbox
        Functions.AutoSwitchCheckboxStatus(self , widgets)

        # /////////////////////////////////////////////////
        # customs css cho btn_profile ở task top
        # sound opening
        Functions.OpenSoundApp(self)


    def SubjectSetupTableManage(self):
        QTableTools.SubjectNewHorizontalHeader(self , widgets)


        QTableTools.SubjectHiddenColumn(self , widgets)

        # ///////////////////////////////////////////////
        # giới hạn chiều rộng của cột
        QTableTools.SetColumnWidthTableWidget(self , widgets)

    # /////////////////////////////////
    # Subject connect các button
    def SubjectConnectButton(self):
        # //////////////////////////////////////////////////////////
        widgets.btn_hide.clicked.connect(lambda: Functions.AnimationSwitchMenu(self, widgets))
        widgets.btn_hide_icons.clicked.connect(lambda: Functions.AnimationSwitchMenu(self, widgets))
        # //////////////////////////////////////////////////////////

        widgets.btn_maximum.clicked.connect(lambda: Functions.ResizeMode(self, widgets))
        widgets.btn_minimum.clicked.connect(lambda: self.showMinimized())

        widgets.btn_close.clicked.connect(lambda: self.close())

        # //////////////////////////////////////////////////////////
        # Functions button clicked connect

        widgets.btn_add.clicked.connect(self.window_additem)
        widgets.btn_proxy.clicked.connect(self.window_proxies)

        # /////////////////////
        # load lại dữ liệu
        widgets.btn_refresh.clicked.connect(self.ComboboxFileActivedConnect)

        # //////////////
        # cài dặt kịch bản
        
        widgets.btn_plan_tool.clicked.connect(self.WidgetFrameScheme)

        widgets.btn_back.clicked.connect(self.SwapWidgetFrameHome)

    # //////////////////////
    # chuyển đổi frame màn hình của stack widget
    # Màn hình quản lý 
    def SwapWidgetFrameHome(self):
        widgets.stackedWidget.setCurrentWidget(widgets.HomePage)
    
    # Màn hình kịch bản
    def WidgetFrameScheme(self):
        widgets.stackedWidget.setCurrentWidget(widgets.PlanPage)

        SubjectQList.ShowCardItems(self , widgets)


    # ///////////////////////////////////////////////
    # Xóa thanh tiêu đề và xử lý di chuyển
    def RemoveWindowFlags(self):
        self.ResetOverLay()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window  )
        self.setAttribute(Qt.WA_TranslucentBackground)

        # ///////////////////////////
        # xử lý di chuyển ứng dụng
        self.resize = Resize(self)



    # ///////////////////////////////////////
    # Tự đồng tạo danh mục mặc định và load item lên combobox danh mục

    def SQLProcessing(self):
        # /////////////////////////////////////////////////////////////
        # SQL
        # tạo thư mục mặc định
        SubjectSQL.CreateTableNew(self, name= "ALL",widgets=widgets)

        # /////////////////////////////////////////////
        SubjectProcessFile.LoadNameTabelSQL(self , widgets)

        # ////////////////////////////
    

    # ////////////////////////////////////////////////////
    # phần này tạo button có hình đại diện , thêm hiệu ứng đăng xuất , thông tin profile tóm tắt

    def MenuButtonProfileUser(self):
        Functions.set_icons(self , widgets)
        self.menu = QMenu()
        self.menu.addAction(QAction("Sign out", self))
        self.menu.addAction(QAction("Settings", self))
        widgets.btn_profile.setMenu(self.menu)

    
    # /////////////////
    # Làm mờ giao diện chính
    def ShowOverLay(self):
        self.filloverlay = Overlay(self)
        self.filloverlay.show()
    
    def ResetOverLay(self):
        try:
            self.filloverlay.close()
        except Exception as Keys:
            print(Keys)

    # /////////////////////////////////////
    # GUI thêm dữ liệu

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
    def window_additem(self):
        # code sql/300
        self.ShowOverLay()
        Namecategory =  widgets.ComboboxFile.currentText()
        NameaccountType =  widgets.ComboBoxTypeAccount.currentText()

        # Call Functions Connect UI
        # Chức năng hiển thị GUI thêm dữ liệu tài khoản
        # Call Sub from Functions Show UI Clone
        window_widgets , windows_ui = Ui_Connect.show_ui(self, Ui_TabWidget)
        window_widgets.tabWidget.setCurrentIndex(0)

        # ///////////////
        # căn giữa
        self.center(windows_ui)
        # toggle frame, button to shadow
        Functions.ShadowFrameConditional(self , window_widgets.label , QColor(0,0,10,40))
        Functions.ShadowFrameConditional(self , window_widgets.frame_3 , QColor(0,0,10,40))
        Functions.ShadowFrameConditional(self , window_widgets.frame_8 , QColor(0,0,10,40))
        Functions.ShadowFrameConditional(self , window_widgets.frame_5 , QColor(0,0,10,40))
        Functions.ShadowFrameConditional(self , window_widgets.item_close , QColor(0,0,10,40))
        Functions.ShadowFrameConditional(self , window_widgets.item_add , QColor(0,0,10,60))

        # data processing
        self.SubjectDataProcessingQThread = SubjectDataProcessing(window_widgets)
        self.SubjectDataProcessingQThread.signal.connect(self.signalSubjectDataProcessing)
        window_widgets.plain_item.textChanged.connect(self.startSubjectDataProcessing)

        window_widgets.item_add.clicked.connect(lambda : self.SubjectDataProcessingConfirm(window_widgets , windows_ui))
        window_widgets.item_close.clicked.connect(lambda : windows_ui.close())
        window_widgets.item_close.clicked.connect(lambda: self.RemoveWindowFlags())
        window_widgets.plain_item.setPlaceholderText("Nhập tài khoản ...")
        window_widgets.plain_item.setPlainText("...")
        window_widgets.plain_item.clear()

        # add list folder
        items = SubjectSQL.GetSQLTable(self)
        items.remove("ALL")
        window_widgets.combo_danhmuc.addItems(items)
        window_widgets.combo_danhmuc.setCurrentText(Namecategory)

        window_widgets.combo_account.setCurrentText(NameaccountType)
        window_widgets.combo_ua.setCurrentText("Windows")

        # Apply blur effect before showing the window
        windows_ui.show()

        # Remove blur effect when window is closed

    # /////////////////////////////
    # chạy QThread xử lý định dạng dữ liệu và gán cho DataProcessingFill
    def startSubjectDataProcessing(self):
        if not self.SubjectDataProcessingQThread.isRunning():
            self.SubjectDataProcessingQThread.start()
    def signalSubjectDataProcessing(self , data : tuple):
        global DataProcessingFill 
        DataProcessingFill = data

    # /////////////////////
    # ga
    def SubjectDataProcessingConfirm(self , window_widgets , window_ui):
        global DataProcessingFill , processing_thread
        # ///////////////////////////////
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
        
        # ////////////////////////////
        # xử lý dữ liệu và gửi tới hàm on_processing
        
        processing_thread = ProcessingThread(window_widgets , DataProcessingFill , textCurrent)

        # /////////////////////////////
        # truyền dữ liệu tới OnProcessingFinished() khi hoàn thành xong task và show lên table
        processing_thread.processing_finished.connect(self.OnProcessingDataFinished)
        processing_thread.start()

        # ///////////////////////////
        # đòng cửa sổ nhập
        window_ui.close()

    # //////////////////////
    # xóa các dữ liệu hiển thị và thêm dữ liệu ở mục chỉ định
    def ComboboxFileActivedConnect(self):
        global DataFillProcess
        
        widgets.TableManage.clear()
        # ///////////////////////////////
        # Config lại headerhorizontal 
        self.SubjectSetupTableManage()
        self.total_items, self.batch_size, self.current_batch = int(1e7) , 1000 , 0
        if widgets.ComboboxFile.currentText() == "ALL":
            ListName = SubjectSQL.GetSQLTable(self)
        else:
            ListName = [widgets.ComboboxFile.currentText()]
        DataFillProcess = SubjectProcessFile.GetDataFromTable(self , ListName)
        self.ProcessingQThreadDataItemsCondition(DataFillProcess)
        Functions.UpdateLabelTotalAccount(self , widgets , len(DataFillProcess))

    
    def OnProcessingDataFinished(self , res : dict, widgets_ : object):
        global DataFillProcess
        # /////////////////////////////////////////////
        # gán dữ liệu đã xử lý để gửi tới hàm thêm dữ liệu
        DataFillProcess = res
        
        self.SubjectOnProcessingDataFinished = SubjectOnProcessingDataFinished(widgets, self.NameCategory , DataFillProcess)
        self.SubjectOnProcessingDataFinished.signal.connect(self.signalOnProcessingDataFinished)
        self.startOnProcessingDataFinished()

                                #       , Ui_main , [{},{} ...]      , ["","" ...]

    def signalOnProcessingDataFinished(self , data : list):
        global DataFillProcess 
        DataFillProcess = data
        # self.ProcessingQThreadDataItemsCondition(DataFillProcess)
        self.ComboboxFileActivedConnect()
        # ////////////////////////////////////////
        # cập nhật thông số tài khoản
        msg.SendMsg(("Thêm thành công !",                1))
        Functions.UpdateLabelTotalAccount(self , widgets , len(DataFillProcess))

    def startOnProcessingDataFinished(self):
        if not self.SubjectOnProcessingDataFinished.isRunning():
            self.SubjectOnProcessingDataFinished.start()

    def window_proxies(self):
        # ///////////////////////////////////
        self.ShowOverLay()
        window_widgets , windows_ui = Ui_Connect.show_ui(self, Ui_TabWidget)
        window_widgets.tabWidget.setCurrentIndex(1)
        self.center(windows_ui)
        # window_widgets -> Object : sử dụng để gọi các frame , button ...
        # window_ui      -> OBject : sử dụng để close , show , công dụng như hàm self.show()
        # Call Functions Connect UI


        # //////////////////////////////////
        # Call Sub from Functions Show UI Clone PROXIES
        # window_widgets.item_add.clicked.connect(lambda : self.SubjectDataProcessingConfirm(window_widgets , windows_ui))
        window_widgets.item_closeProxy.clicked.connect(lambda : windows_ui.close())
        window_widgets.item_closeProxy.clicked.connect(lambda: self.RemoveWindowFlags())

        # ///////////////////////////////////
        # toggle frame, button to shadow

        # ///////////////////////////////////////////////
        # run , check script


    # ///////////////////////////////////////////////////////////////
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

    def mousePressEvent(self, event):
        self.resize.mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.resize.mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        self.resize.mouseMoveEvent(event)
    # /////////////////////////////////////////
    # hiệu ứng làm tròn viền
    def paintEvent(self, event):
        painter = QPainter(self)
        path = QPainterPath()
        if self.isMaximized():
            # ////////////////////////////////////
            # full màn và cạnh nhọn
            path.addRoundedRect(0, 0, self.width(), self.height(), 0, 0)
        else:
            # ////////////////////////////////////
            # full màn và cạnh tròn
            path.addRoundedRect(0, 0, self.width(), self.height(), 10, 10)

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillPath(path, QBrush(QColor(38, 49, 98)))
        painter.setPen(QColor(94,112,167))
        painter.drawPath(path)
    # ///////////////////////////////////////////////////////////////

    # ////////////////////////////////
    # hiệu ứng thông báo tin nhắn

    # ///////////////////////////////
    # hiển thị ở góc màn hình ứng dụng
    def _on_resize(self, event):
        msg.move_notification()
        QMainWindow.resizeEvent(self, event)
    # /////////////////////////////////
    # hiển thị 100 dòng dữ liệu 
    def ProcessingQThreadDataItemsCondition(self , data : dict):
        # //////////////////////////////////
        # xử lý 1000 dữ liệu và hiển thị với QThread
        self.thread = DataGenerator(self.total_items, self.batch_size, self.current_batch , data)
        self.thread.data_signal.connect(self.SubjectShowLoadData)
        self.thread.start()

        # ///////////////////
        # thông báo hiển thị

    # //////////////////////////////////////////////////////////
    # thêm dữ liệu từ mảng vào bảng
    # [{}...]
    def SubjectShowLoadData(self, data):
        # Vô hiệu hóa chế độ chọn và thiết lập chế độ chọn theo hàng
        # Tắt selection
        widgets.TableManage.setSelectionMode(QTableWidget.NoSelection)
        widgets.TableManage.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Xác định chỉ số cột cho 'message' và 'c_user'
        message_column_index = index_name.get("message", -1)
        c_user_column_index = index_name.get("c_user", -1)

        # Thiết lập delegate cho cột 'message' và 'c_user'
        if message_column_index != -1:

            widgets.TableManage.setItemDelegateForColumn(message_column_index, RoundedBorderDelegate(self,color=QColor(70, 200, 245), bold=1))

        if c_user_column_index != -1:
            widgets.TableManage.setItemDelegateForColumn(c_user_column_index, RoundedBorderDelegate(self,color=QColor(0, 204, 204), bold=1))

        # Thêm dữ liệu vào bảng
        for row_data in data:
            try:
                # Lấy vị trí hàng hiện tại và chèn hàng mới
                row_position = widgets.TableManage.rowCount()
                widgets.TableManage.insertRow(row_position)

                # Thêm item checkbox vào cột đầu tiên
                widgets.TableManage.setItem(row_position, 0, QTableTools.CheckboxNew(self))

                # Thêm item số hàng vào cột thứ hai
                item_count = QTableTools.SubjectItemsText(
                    self, text=str(row_position + 1), color=QColor(255,255,255), size_font=8)
                widgets.TableManage.setItem(row_position, 1, item_count)

                # Thiết lập chiều cao hàng
                widgets.TableManage.setRowHeight(row_position, 40)

                # Thêm các item dữ liệu vào các cột tương ứng
                for temp_name, value in row_data.items():
                    try:
                        # Xác định màu sắc dựa trên tên cột
                        color = QColor(20, 57, 39)  # Màu mặc định
                        if temp_name == "message":
                            value = time_lastest(value)
                            color = QColor(255,255,255)
                        elif temp_name == "c_user":
                            color = QColor(92, 0, 230)
                        else:
                            color =  QColor(255,255,255)
                        # Tạo item với màu sắc và kích thước font đã chỉ định
                        if temp_name == "work":
                            value = json.loads(open("./models/json/config.json","r",encoding="utf-8").read())["account.work"]
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
    # Tăng giá trị biến đếm batch hiện tại
        self.current_batch += 1

        # //////////////////////////////////////
        # thêm hiệu ứng selection line

        QTableTools.AddSelectionItems(self , widgets)
    

    # ////////////////////////////////////////////
    # check cuộn xuống 100 dòng sẽ load thêm
    def SubjectAutoLoadData(self):
        scrollbar = widgets.TableManage.verticalScrollBar()
        scrollbar.valueChanged.connect(lambda :QTableTools.HandleScroll(self,scrollbar,DataFillProcess))
        header = widgets.TableManage.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

    # /////////////////////////////////////////////////
    # search

    def search(self):
        try:
            self.processingSearch = Search(widgets,widgets.line_search.text().lower())
            self.startprocessingSearch()
        except Exception as KeyError:
            print(KeyError)
    
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
        
    # ////////////////////////////////
    # Custom các frame

    def CustomShadowFrameApp(self):
        # //////////////////////////////////////////////////////////
        # shadow effect frame_manage_tool , ... frame as 
        Functions.ShadowFrameConditional(self , widgets.scrollArea_manage , QColor(1, 1, 1, 20))

        Functions.ShadowFrameConditional(self , widgets.frame_manage_main , QColor(1, 1, 1, 80))

        widgets.frame_manage_tool.setStyleSheet("QFrame{border-radius:10px;}")
        Functions.ShadowFrameConditional(self , widgets.frame_manage_tool , QColor(1, 1, 10, 50))

        widgets.frame_status_manage.setStyleSheet("QFrame{border-radius:10px;}")
        Functions.ShadowFrameConditional(self , widgets.frame_status_manage , QColor(1, 1, 10, 80))

        Functions.ShadowFrameConditional(self , widgets.frame_tool_two , QColor(0, 0, 10, 50))
    
    
    # /////////////////////////////
    # phần này tạo icons khi di chuyển
    def EdgeGripShort(self):
        # ///////////////////////////////////
        # tạo icon kéo dãn khi di chuột gần mép
        self.left_grip = EdgeGrip(widgets.centralwidget, Qt.LeftEdge)
        self.right_grip = EdgeGrip(widgets.centralwidget, Qt.RightEdge)
        self.top_grip = EdgeGrip(widgets.centralwidget, Qt.TopEdge)
        self.bottom_grip = EdgeGrip(widgets.centralwidget, Qt.BottomEdge)
    

    # ///////////////////////
    # mô phỏng kéo dài cho các cột
    def InteractiveHeader(self):
        header = widgets.TableManage.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    checkbox_style = CheckBoxStyle(app.style())
    app.setWindowIcon(QIcon("./icons/logo/icons.png"))
    window = WindowInterface()
    sys.exit(app.exec_())
