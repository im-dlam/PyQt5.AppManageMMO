import sqlite3
from datetime import datetime
import pathlib
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
    def SQLRemoveAccount(self, uid):
        your_dir  = pathlib.Path.cwd()
        with open(f'{your_dir}/models/bin/facebook.bin', 'a',encoding='utf-8') as file:
            # Lấy danh sách tất cả các bảng, bỏ qua bảng 'ALL'
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in self.cursor.fetchall()]
            
            if 'ALL' in tables:
                tables.remove('ALL')
            
            # Duyệt qua từng bảng
            for table in tables:
                try:
                    # Kiểm tra xem bảng có cột 'c_user' hay không
                    self.cursor.execute(f"PRAGMA table_info({table})")
                    columns = [column[1] for column in self.cursor.fetchall()]
                    
                    if 'c_user' in columns:
                        # Lấy các hàng cần xóa
                        select_cmd = f"SELECT * FROM {table} WHERE c_user = ?"
                        self.cursor.execute(select_cmd, (uid,))
                        rows = self.cursor.fetchall()
                        
                        # Lưu dữ liệu vào file
                        for row in rows:
                            # Lưu dữ liệu theo định dạng column1|column2|...
                            row_data = '|'.join(map(str, row))  # Chuyển từng giá trị trong hàng thành chuỗi
                            file.write(f"{row_data}\n")
                        
                        # Xóa dữ liệu sau khi lưu
                        delete_cmd = f"DELETE FROM {table} WHERE c_user = ?"
                        self.cursor.execute(delete_cmd, (uid,))
                        print(f"Deleted rows in table {table} where c_user = {uid}")
                    else:
                        print(f"Skipping table {table} - column 'c_user' does not exist.")
                
                except Exception as e:
                    print(f"Skipping table {table} due to error: {e}")
        
        # Lưu thay đổi vào cơ sở dữ liệu
        self.connect.commit()

        
        # Lưu các thay đổi vào cơ sở dữ liệu
    def GetDataFromUID(self, uid):
        return self.cursor.execute(f"SELECT * FROM {self.name} WHERE c_user = ?", (uid,)).fetchall()
    def SQLUpdateDataFromKey(self,temp_:hash):
        """ 
        **Nhập đầu vào là 1 hash**
        
              `~ {key}     : tên dữ liệu cần đổi `<br>
              `~ {content} : nội dung cần cập nhật của key`<br>
              `~ {id}      : key số user_id liệu để cập nhật theo chỉ định`<br>
        
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
        self.cursor.execute(f"UPDATE {self.name} SET {key} = ? WHERE c_user = ?", (content_update, id))
        self._close()
    
    def SQLGetDataFromName(self):
        self.cursor.execute(f'''SELECT  * FROM "{self.name}"''')
        return self.cursor.fetchall()
    
    def SQLGetTableName(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # //////////////////////////
        # name = ("",)
        return [name[0] for name in self.cursor.fetchall()]
    