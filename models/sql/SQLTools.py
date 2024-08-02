from models import *
from models.sql.SQLModules import *
import re
class SubjectSQL:
    def CreateTableNew(self,name,widgets):
        vietnamese_characters = re.compile(
            r'[\u00C0-\u00C3\u00C8-\u00CA\u00CC-\u00CD\u00D2-\u00D5\u00D9-\u00DA\u00DD'
            r'\u00E0-\u00E3\u00E8-\u00EA\u00EC-\u00ED\u00F2-\u00F5\u00F9-\u00FA\u00FD'
            r'\u0102\u0103\u0110\u0111\u0128\u0129\u0168\u0169\u01A0\u01A1\u01AF\u01B0]'
        )
        msg = Notification(widgets.centralwidget)

        if bool(vietnamese_characters.search(name)):
            msg.SendMsg(
                ("Unsupported Text Vietnamese" ,     0)
            )
            return
        tweet = SQL(name).SQLNewTable()
        if name != "ALL":
            msg.SendMsg(tweet)
        
        return tweet[1]
    
    def DeleteTableName(self , name , widgets):
        msg = Notification(widgets.centralwidget)
        SQL(name).SQLDeleteTable()
        msg.SendMsg(("Xóa thành công danh mục ({}) !".format(name),   1))
        

    def GetSQLTable(self):
        return SQL("").SQLGetTableName()
    

    def AddAccountTable(self , name , data , widgets):
        for data_ in data:
            SQL(name).SQLInsertDataFromName(data=data_)



    def ProcessGetDataTable(self , name):

        fill = []
        dataResult = SQL(name).SQLGetDataFromName()
        for tinhiu in dataResult:
            (id ,
            c_user ,
            password ,
            code ,
            cookie ,
            access_token ,
            email ,
            passemail ,
            user_agent ,
            proxy ,
            mailkp ,
            passmailkp ,
            phone ,
            birthday ,
            status ,
            work,
            message) =  tinhiu

            fill.append(
                {
                    "c_user":c_user,
                    "password":password,
                    "code":code,
                    "cookie":cookie,
                    "access_token":access_token,
                    "email":email,
                    "passemail":passemail,
                    "user-agent":user_agent,
                    "proxy":proxy,
                    "mailkp":mailkp,
                    "passmailkp":passmailkp,
                    "phone":phone,
                    "birthday":birthday,
                    "status":status,
                    "work":work,
                    "message":message
                }
            )
        return fill

    def _on_resize(self, event):
        msg.move_notification()
        QMainWindow.resizeEvent(self, event)

