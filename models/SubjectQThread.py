from main import *
from . SubjectTools import *
from . Ui_Functions import *
from . SubjectFileName import *
# ///////////////////
# xử lý lọc form nhập ở gui
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
        if DataProcessingFill[0] != [] and DataProcessingFill[0][0]["c_user"]  :
            
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

            Functions.ComboboxProcessItem(self , window_widgets  , line_[index-1].strip("\n") , data)

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
            self.t.moveToThread(self)  # Di chuyển QTimer vào luồng hiện tại
            self.t.timeout.connect(self.GetDataFromTable)
            self.t.start(1000)  # Bắt đầu timer, kiểm tra mỗi 2 giây
            self.exec_()  # Bắt đầu vòng lặp sự kiện của QThread
        self.terminate()
    def GetDataFromTable(self):
        process = []
        for name in self.NameCategory:
            process += SubjectSQL.ProcessGetDataTable(self, name)
        self.signal.emit(process)

        if len(process) == self.total:
            self.t.stop()
            self.quit()
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
