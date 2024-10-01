from PyQt5.QtCore import QObject
from main import *
from .SubjectTools import *
from .Ui_Functions import *
from .FileName import *
import requests
# ///////////////////
# xử lý lọc form nhập ở gui
class LoadNewData(QThread):
    def __init__(self,widgets,data) :
        super(LoadNewData,self).__init__()
        self.widgets = widgets
        self.data =  data
    
    def run(self):
        self.widgets.TableManage.setSelectionMode(QTableWidget.NoSelection)
        self.widgets.TableManage.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Xác định chỉ số cột cho 'message' và 'c_user'
        message_column_index = index_name.get("message", -1)
        c_user_column_index = index_name.get("c_user", -1)

        
        # Thiết lập delegate cho cột 'message' và 'c_user'
        if message_column_index != -1:

            self.widgets.TableManage.setItemDelegateForColumn(message_column_index, RoundedBorderDelegate(self,color=QColor(70, 200, 245), bold=1))

        if c_user_column_index != -1:
            self.widgets.TableManage.setItemDelegateForColumn(c_user_column_index, RoundedBorderDelegate(self,color=QColor(0, 204, 204), bold=1))

        # END
        
        # Thêm dữ liệu vào bảng

        for row_data in self.data:
            try:


                
                # Lấy vị trí hàng hiện tại và chèn hàng mới
                
                row_position = self.widgets.TableManage.rowCount()
                self.widgets.TableManage.insertRow(row_position)

                
                # Thêm item checkbox vào cột đầu tiên
                self.widgets.TableManage.setItem(row_position, 0, QTableTools.CheckboxNew(self))

                
                # Thêm item số hàng vào cột thứ hai
                
                item_count = QTableTools.SubjectItemsText(
                    self, text=str(row_position + 1), color=QColor(255,255,255), size_font=8)
                self.widgets.TableManage.setItem(row_position, 1, item_count)


                
                # Thiết lập chiều cao hàng
                
                self.widgets.TableManage.setRowHeight(row_position, 40)

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


                        # END

                        # Tạo item với màu sắc và kích thước font đã chỉ định
                        
                        if temp_name == "work":
                            typeAccount = 'Facebook'.lower()
                            # typeAccount = self.widgets.ComboBoxTypeAccount.currentText().lower()
                            value = str(len(json.loads(open("./models/json/config.json","r",encoding="utf-8").read())["account.work"][typeAccount])) + " Actions !"
                        elif temp_name == "proxy":
                            if ":" not in  value:
                                value = "Local IP"
                        elif temp_name == "status":
                            if value == "Unknown":
                                color =  QColor(250,250,250)
                            elif value == "LIVE":
                                color =  QColor(64, 191, 128)
                            else:
                                color = QColor(255, 84, 135)
                        item_category = QTableTools.SubjectItemsText(
                            self, text=str(value), color=color, size_font=8)
                        
                        # Thêm item vào bảng ở vị trí hàng và cột tương ứng
                        if temp_name == "status":
                            if value == "Unknown":
                                item_category.setIcon(QIcon(r".\icons\png\icons8-dot-24.png"))
                            elif value == "LIVE":
                                item_category.setIcon(QIcon(r".\icons\png\icons8-dot-24_live.png"))
                            else:
                                
                                item_category.setIcon(QIcon(r".\icons\png\icons8-dot-24_red.png"))
                        elif temp_name == "work":
                            item_category.setIcon(QIcon(r".\icons\png\icons8-thunder-24.png"))
                        self.widgets.TableManage.setItem(row_position, index_name[temp_name], item_category)

                    except KeyError:
                        # Bỏ qua nếu không tìm thấy chỉ số cột
                        continue

            except Exception as e:
                # In ra thông báo lỗi nếu có
                print(f"Error adding row data: {e}")


class CheckFacebook(QThread):
    signal =  pyqtSignal(object)
    def __init__(self, infoID):
        super(CheckFacebook,self).__init__()
        self.infoID = infoID
    def getDataFromSQL(self,uid):

        nameSQL =  SubjectSQL.GetSQLTable(self)    
        for name in nameSQL:
            if name == 'ALL':continue
            depos = SQL(name).GetDataFromUID(uid)
            if depos != []:
                return name
    def startCheck(self,UID):
        name = self.getDataFromSQL(UID)
        obj = {'SQL':name}
        r =  requests.get(f'https://graph.facebook.com/{UID}/picture?redirect=0').json()
        if r.get('data',{}).get('height',{}) == {}:
            obj.update({'msg':f"{UID} DIE",'code':300,'uid':UID})
        else:
            obj.update({'msg':f"{UID} LIVE",'code':200,'uid':UID})
        self.signal.emit(obj)
    def run(self):
        for uid in self.infoID:
            threading.Thread(target=(self.startCheck),args=(uid,)).start()

class ProxySQL(QThread):
    def __init__(self):
        super(ProxySQL,self).__init__()

    def  run(self):
        filedumps = json.loads(open(your_dir_config,"r",encoding="utf-8").read())
        onProxy = filedumps['config']['id.Proxy']
        onAutoProxy =  filedumps['config']['id.Proxyauto']
        proxyList = filedumps['proxy']['list']
        proxyList.remove('')
        listSQL = SubjectSQL.GetSQLTable(self) # name sql []
        index = 0
        for name in listSQL:
            data_from_name = SubjectSQL.ProcessGetDataTable(self , name)
            for idx , getstr in enumerate(data_from_name):

                if onAutoProxy and onProxy:
                    if proxyList == []:continue
                    if index == len(listSQL) and proxyList != []:
                        index = 0
                    send = {'key':'proxy','content':proxyList[index],'id':getstr['c_user']}
                    index += 1
                else:
                    if len(proxyList) == idx:
                        return
                    send = {'key':'proxy','content':proxyList[idx],'id':getstr['c_user']}
                SQL(name).SQLUpdateDataFromKey(send)
class SubjectDataProcessing(QThread):
    signal = pyqtSignal(tuple)
    def __init__(self, window_widgets):
        super(SubjectDataProcessing, self).__init__()
        self.window_widgets = window_widgets

    def run(self):
        ResultData = self.SubjectDataProcessing(self.window_widgets)

        # /////////////////
        # truyền dữ liệu về file main
        if ResultData == None:
            ResultData = (None , None)
        self.signal.emit(ResultData)
    def SubjectDataProcessing(self, window_widgets):
        global DataProcessingFill
        # Code cho SubjectDataProcessing của bạn
        textOut = window_widgets.plain_item.toPlainText()
        line_ = textOut.split("\n")
        DataProcessingFill =  convert_data(textOut) , textOut
        if DataProcessingFill[0] != [] and DataProcessingFill[0][0]["c_user"] :
            
            # ////////////////////////////
            # tìm kiếm chuỗi dữ liệu đầy đủ nhất
            min_  , index = [0] * (len(line_) + 1 ) , 0
            for i , dp in enumerate(line_,start=1):
                dp = dp.replace("||","|")

                min_[i] = max(min_[i-1] , len(dp.split("|")))

                if min_[i] > min_[i-1]:index = i
            # //////////////////////////////
            data = convert_data(line_[index-1].strip("\n"))[0]
            # ///////////////////////////////
            # show item lên table
            Functions.ComboboxProcessItem(self , window_widgets  , line_[index-1].strip("\n") , data)
        elif line_ != "":
            Functions.ComboboxProcessItem(self , window_widgets  , "" , [])


        # ///////////////////////////
        # set total account
        window_widgets.label.setText(
            f"TOTAL:  {len(DataProcessingFill[0])}"
            )
        return DataProcessingFill
    

class GetDataThread(QThread):
    signal = pyqtSignal(object)
    def __init__(self, widgets, NameCategory, total):
        super(GetDataThread, self).__init__()
        self.widgets = widgets
        self.NameCategory = [NameCategory]
        self.total = total
    def run(self):

        
        self.t = QTimer()
        for _ in range(10):
            try:
                self.t.moveToThread(self)  # Di chuyển QTimer vào luồng hiện tại
                self.t.timeout.connect(self.GetDataFromTable)
                self.t.start(1000)  # Bắt đầu timer, kiểm tra mỗi 2 giây
                self.exec_()  # Bắt đầu vòng lặp sự kiện của QThread
            except:
                self.terminate()
                self.quit()
    def GetDataFromTable(self):
        process = []
        for name in self.NameCategory:
            process += SubjectSQL.ProcessGetDataTable(self, name)
        self.signal.emit(process)

class SubjectOnProcessingDataFinished(QThread):
    signal = pyqtSignal(object)

    def __init__(self, widgets, NameCategory, DataFillProcess):
        super(SubjectOnProcessingDataFinished, self).__init__()
        self.widgets = widgets
        self.NameCategory = NameCategory
        self.DataFillProcess = DataFillProcess

    def run(self):
        SubjectProcessFile.InsertDataInTabel(self, self.NameCategory, self.DataFillProcess, self.widgets)
# ////////////////////////
# xử lý định dạng
class ProcessingThread(QThread):
    processing_finished = pyqtSignal(list , object)  # Tín hiệu để thông báo khi xử lý xong

    def __init__(self, widgets , data: tuple, line: dict, parent=None):
        super().__init__(parent)
        self.widgets = widgets
        self.data = data
        self.line = line
    def run(self):
        data_process, data_line = self.data
        _data_process = []
        data_line = data_line.split("\n")
        for hash_line in data_line:
            if hash_line == "\n":continue
            _line_data = {
                    "c_user": "",
                    "password": "",
                    "code": "",
                    "cookie": "",
                    "access_token": "",
                    "email": "",
                    "passemail": "",
                    "user-agent": "",
                    "proxy": "",
                    "mailkp":"",
                    "passmailkp":"",
                    "phone":"",
                    "birthday":"",
                    "status":"",
                    "work":"",
                    "message":""
                    }
            for i , name_value in enumerate(self.line) :
                if name_value != "":
                    try:
                        _line_data.update({name_value: hash_line.split("|")[i]})
                    except:continue
            

            _data_process.append(_line_data)
        
        # Émet tín hiệu khi xử lý xong
        self.processing_finished.emit(_data_process , self.widgets)
