from PyQt5.QtCore import QObject
from main import *
from . SubjectTools import *
from . Ui_Functions import *
from . SubjectFileName import *
# ///////////////////
# xử lý lọc form nhập ở gui



class ProxySQL(QThread):
    def __init__(self):
        super(ProxySQL,self).__init__()

    def  run(self):
        filedumps = json.loads(open(your_dir_config,"r",encoding="utf-8").read())
        onProxy = filedumps['config']['id.Proxy']
        onAutoProxy =  filedumps['config']['id.Proxyauto']
        proxyList = filedumps['proxy']['list']

        listSQL = SubjectSQL.GetSQLTable(self) # name sql []
        index = 0
        for name in listSQL:
            data_from_name = SubjectSQL.ProcessGetDataTable(self , name)
            for idx , getstr in enumerate(data_from_name):

                if onAutoProxy and onProxy:
                    if index == len(listSQL):index = 0
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
