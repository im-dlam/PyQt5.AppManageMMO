from models import *

class SubjectProcessFile:
    def __init__(self) -> None:
        pass


    def LoadNameTabelSQL(self , widgets):
        # ////////////////
        # Get danh sách table
        widgets.ComboboxFile.clear()
        SQLName  =  SubjectSQL.GetSQLTable(self)

        # Thêm danh sách name table lên tiêu đề thư mục
        widgets.ComboboxFile.addItems(SQLName)
        # ////////////////////////
        widgets.ComboboxFile.setCurrentText("ALL")
    

    def InsertDataInTabel(self , name , data:dict , widgets):
        TextItems = ["c_user","password","code","cookie","access_token","email","passemail","user-agent","proxy","mailkp","passmailkp","phone","birthday"]
        for tada in data:
             # //////////////////////////////////
             # check name
             for name_value in TextItems:
                 tada.update({name_value:""}) if name_value not in tada else None
        
        SubjectSQL.AddAccountTable(self,name= name , data=data , widgets=widgets)
    

    def GetDataFromTable(self , __name):
        process = []
        for name in __name:
            process += SubjectSQL.ProcessGetDataTable(self , name)
        
        return process

    
    
