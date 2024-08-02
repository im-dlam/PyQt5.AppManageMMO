import sqlite3
from datetime import datetime

class SQL:
    def __init__(self , name):

        """
        **name : tên của table **
        """
        # /////////////////////////////////
        # kết nối dữ liệu
        self.connect = sqlite3.connect('./models/sql/database.db')
        self.name    = name
        self.cursor  = self.connect.cursor()
    
    def _close(self):
        self.connect.commit()
        self.connect.close()
    def SQLCheckExist(self):
        if self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (self.name,)).fetchone() == None:
            return 0
        
        return 1
    def SQLNewTable(self):

        if self.SQLCheckExist():
            return ("Danh mục đã tồn tại !",            0)
        self.cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS "{self.name}" (
            id INTEGER PRIMARY KEY,
            c_user TEXT,
            password TEXT,
            code TEXT,
            cookie TEXT,
            access_token TEXT,
            email TEXT,
            passemail TEXT,
            user_agent TEXT,
            proxy TEXT,
            mailkp TEXT,
            passmailkp TEXT,
            phone TEXT,
            birthday TEXT,
            status TEXT,
            work TEXT,
            message TEXT
        )
        ''')

        return ("Tạo danh mục thành công !",        1)
    
    def SQLInsertDataFromName(self , data : hash):
        """
         **data **: Dữ liệu dạng hash đầy đủ bảng key<br>
         **bảng key**:
             ~ id
             ~ c_user
             ~ password
             ~ code
             ~ cookie
             ~ access_token
             ~ email
             ~ passemail
             ~ user_agent
             ~ proxy
             ~ mailkp
             ~ passmailkp
             ~ phone
             ~ birthday
        """

        c_user = data["c_user"]
        code   = data["code"]
        password = data["password"]
        cookie   = data["cookie"]
        access_token = data["access_token"]
        email        = data["email"]
        passemail    = data["passemail"]
        user_agent   = data["user-agent"]
        proxy        = data["proxy"]
        mailkp       = data["mailkp"]
        passmailkp   = data["passmailkp"]
        phone        = data["phone"]
        birthday     = data["birthday"]

        self.cursor.execute(f'''
            INSERT INTO "{self.name}" (
            c_user  ,password, code, cookie, access_token, email, passemail, user_agent, proxy, mailkp, passmailkp, phone, birthday, status ,work , message 
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? , ? , ?)
            ''', (c_user, password, code,cookie, access_token, email, passemail, user_agent, proxy, mailkp, passmailkp, phone, birthday , "Unknown" ,"" , f"{datetime.now()}"))
        self.cursor.execute(f'''SELECT  * FROM "{self.name}"''')
        self._close()
    def SQLDeleteTable(self):
        self.cursor.execute(f"DROP TABLE IF EXISTS '{self.name}'")
        self._close()
    
    def SQLUpdateDataFromKey(self,temp_:hash):
        """ 
        **Nhập đầu vào là 1 hash**
        
              `~ {key}     : tên dữ liệu cần đổi `<br>
              `~ {content} : nội dung cần cập nhật của key`<br>
              `~ {id}      : key số thứ tự dữ liệu để cập nhật theo chỉ định`<br>
        
         **Danh sách key**<br>: 
             ~ id
             ~ c_user
             ~ password
             ~ code
             ~ cookie
             ~ access_token
             ~ email
             ~ passemail
             ~ user_agent
             ~ proxy
             ~ mailkp
             ~ passmailkp
             ~ phone
             ~ birthday"""
        key = temp_["key"]
        content_update = temp_["content"]
        id  = temp_["id"]
        self.cursor.execute(f"update {self.name} set {key} = '{content_update}' where id = {id}")
        self._close()
    
    def SQLGetDataFromName(self):
        self.cursor.execute(f'''SELECT  * FROM "{self.name}"''')
        return self.cursor.fetchall()
    
    def SQLGetTableName(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # //////////////////////////
        # name = ("",)
        return [name[0] for name in self.cursor.fetchall()]
    