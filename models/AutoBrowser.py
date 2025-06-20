from main import *
from .Pyotp import *
from selenium import webdriver
import random
from selenium_profiles.webdriver import Chrome
from selenium_profiles.profiles import profiles
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from time import sleep
from models import *
import os , sys , shutil

DEPOS_TEMP , QHD , NAME = () ,  0 , str()

class Facebook:
    def __init__(self, driver: WebDriver , signal : pyqtSignal , report: dict):
        global DEPOS_TEMP , QHD
        self.signal =  signal
        self.driver = driver
        self.report = report
        (stt ,
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
        message) = DEPOS_TEMP

        self.stt = stt
        self.c_user = c_user
        self.password = password
        self.code = code
        self.cookie = cookie
        self.access_token = access_token
        self.email = email
        self.passemail = passemail
        self.user_agent = user_agent
        self.proxy = proxy
        self.mailkp = mailkp
        self.passmailkp = passmailkp
        self.phone = phone
        self.birthday = birthday
        self.status = status
        self.work = work
        self.message = message

    @property
    def config(self):
        if not hasattr(self, '_config'):
            self._config = json.loads(open(your_dir_config,'r',encoding='utf-8').read())
        return self._config
    
    @staticmethod
    def TimeWriting():
        sleep(float(random.randrange(1,10)/25))

    @staticmethod
    def TimeWait():
        sleep(float(random.randrange(4,10)/5))

    # KIỂM THỬ PHẦN TỬ TRÁNH BÁO LỖI
    def find_element(self , by : By , value: str):
        for _ in range(3):
            try:
                _driver_ = self.driver.find_element(by , value)
                return _driver_
            except Exception as error :
                msg =  error
                continue
        
        print("_"*50)
        print(f"/ {value} ")
        print(f"/ {msg} ")
        print("_"*50)
        

    def convert_cookie_to_str(self , cookies_for_dict): 
        cookies = "".join(["{name}={value};".format(name=dict_['name'],value=dict_['value']) for dict_ in cookies_for_dict])
        return cookies
    def verify_login(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@class='MAWOembedIframe']"))
            )

            cookies_for_dict = self.driver.get_cookies()
            self.report.update({'code':20032006,'content':self.convert_cookie_to_str(cookies_for_dict),'id':self.report['uid'],'key':'cookie'})
            self.signal.emit(self.report)

            return True
        except:
            return 0

    def Notifications(self):
        try:
            for _ in range(2):
                self.driver.implicitly_wait(10)
                element_nofi = self.find_element(By.XPATH, '//*[@href="/notifications/"]')
                if element_nofi is not None:
                    self.report.update({'code':99,'msg':'click button Notifications'})
                    self.signal.emit(self.report)
                    element_nofi.click()
                    sleep(2)
        except Exception as e:
            print(e)
    
    def Messengers(self):
        for _ in range(2):
            self.driver.implicitly_wait(10)
            element_ = self.find_element(By.XPATH,"(//*[@aria-label='Messenger'])[1]")
            if element_ is not None:
                self.report.update({'code':99,'msg':'click button Messenger'})
                self.signal.emit(self.report)
                self.arguments_click(element_)
                sleep(3)
    
    def SeeMorePosts(self):
        element_ = self.find_element(By.XPATH,'//div[text()="See more"]')
        if element_ is not None:
            self.arguments_click(element_)


    def CommentRead(self):
        element_comment = self.find_element(By.XPATH,'//span[text()="Comment"]')
        if element_comment is not None:
            self.report.update({'code':99,'msg':'click button Comment'})
            self.signal.emit(self.report)
            self.arguments_click(element_comment)
            self.SeeMorePosts()
            self.closeButtonElement()

    
    def closeButtonElement(self):
        self.driver.implicitly_wait(10)
        element_ = self.find_element(By.XPATH,"//*[@aria-label='Close']")
        if element_ is not None:
            self.report.update({'code':99,'msg':'close frame content'})
            self.signal.emit(self.report)
            self.arguments_click(element_)
    def BackToHome(self):
        self.driver.implicitly_wait(10)
        _driver = self.find_element(By.XPATH,'(//a[@href="/"])[1]')
        
        if _driver:
            self.arguments_click(_driver)

    # TỰ ĐỘNG TÌM KIẾM
    def searchFacebook(self):
        self.driver.implicitly_wait(10)
        _wait = self.WaitByXpath('//*[@spellcheck="false" and @role="combobox"]')
        if _wait:
            _driver = self.find_element(By.XPATH , '//*[@spellcheck="false" and @role="combobox"]')
            if _driver:
                self.arguments_click(_driver) # CLICK BUTTON ICON SEARCH
                # TÌM KIẾM NEW
                _driver.send_keys(random.choice(['#new','#trend','#hot','#tintuc','#CNN','#BBC']))
                _driver.send_keys(Keys.ENTER)
                
                self.driver.implicitly_wait(10)
                sleep(3)
                for _ in range(random.randint(20,40)):
                    self.arguments_scroll(1)

                    sleep(random.randint(1,3))

                self.BackToHome()
    # THẢ CẢM XÚC NGẪU NHIÊN
    def ActionReactions(self):
        keyID = {
            0 : 'Like',
            30: 'Love',
            60: 'Haha',
            90: 'Care'
        }
        idRandom = random.choice([0,30,60,90])
        self.driver.implicitly_wait(10)
        element_textLike =  self.find_element(By.XPATH,'//span[text()="Like"]')
        if element_textLike is not None:
            self.report.update({'msg':f'{keyID[idRandom]} Bài viết','code':99})
            self.signal.emit(self.report)
            try:
                ActionChains(self.driver).click_and_hold(element_textLike).perform() # giữ chuột
                sleep(1)
                ActionChains(self.driver).move_to_element_with_offset(element_textLike,idRandom,-30).click().perform()
            except:
                return 

            return keyID[idRandom]
    # DISMISS CHECKPOINT KHÁNG BOT TRÌNH DUYỆT
    def AntiSpam(self):
        if "checkpoint" in self.driver.current_url:
            _driver = self.find_element(By.XPATH,'//*[@aria-label="Dismiss"]')
            if _driver:
                _driver.click()

    def FeedisHome(self):
        person , check , ifp = [4,8,12,16,18,22] , 0 , 4
        timeWork =  datetime.now() + timedelta(minutes=self.config['config']['id.TimeWorking'])
        x_position_scroll , loop_add = 0 , 0
        self.AccountsChangeLanguage()
        while datetime.now() <= timeWork:
            loop_add += 1
            # NGẪU NHIÊN REACTION
            if check:
                ifp = random.choice(person)
                check  = 0

            # THỰC HIỆN CÁC HOẠT ĐỘNG
            if loop_add % ifp == 0:
                self.AntiSpam()
                self.searchFacebook()
                self.ActionReactions()

                self.CommentRead()

                # RANDOM CÁC HÀNH ĐỘNG 
                random.choice([self.Messengers , self.Notifications , self.searchFacebook])()
                check = 1
                # THỜI GIAN NGHỈ
                sleep(random.randint(4,7))
            
            # keo cuon web
            x_position_scroll += random.randint(110,200)
            self.driver.execute_script(f"window.scrollTo(0, {x_position_scroll});")
            self.TimeWriting()

        self.report.update({'code':99,'msg':'close...'})
        self.signal.emit(self.report)
        try:
            self.driver.quit()
        except Exception:
            print("error closing")
        return 99
    def cookies_to_string(self, cookies : str):
        return "".join(["{}={};".format(parse['name'],parse['value']) for parse in cookies])

    # ĐỔI NGÔN NGỮ BẰNG API
    def AccountsChangeLanguage(self):
        driver_ = self.find_element(By.XPATH,'(//*[@id="facebook"])')
        if driver_:
            self.driver.implicitly_wait(10)
            user_agent , cookies_browser   =  self.driver.execute_script('return navigator.userAgent;') , self.driver.get_cookies()
            
            cookies_after_convert , _dtsg =  self.cookies_to_string(cookies_browser) , self.driver.page_source.split(',{"token":"')[1].split('"}')[0]
            lang_browser = driver_.get_attribute('lang')
            if lang_browser != "en":
                script = f"""
                var headers = {{
                    'accept': '*/*',
                    'accept-language': 'en-US;',
                    'content-type': 'application/x-www-form-urlencoded',
                    'cookie': '{cookies_after_convert}',
                    'dnt': '1',
                    'origin': 'https://www.facebook.com',
                    'referer': 'https://www.facebook.com',
                    'sec-ch-ua-platform': '"Windows"',
                    'user-agent': '{user_agent}',
                    'x-fb-lsd': 'UEIdUKYqlMER2LxiAXtnJt'
                }};

                var dataString = 'av={self.c_user}&__aaid=0&__user={self.c_user}&__a=1&__req=15&__hs=19992.HYP%3Acomet_plat_default_pkg.2.1..2.1&dpr=1&__ccg=EXCELLENT&__rev=1016820347&__s=3tkocp%3Afj77or%3A4im4cc&__hsi=7418865971727892589&__dyn=7AzHK4HwBgDx-5Q1hyoyEqxd4Ag5S3G2O5U4e2C3-4UKewSAx-bwNw9G2Saxa0DU6u3y4o27wxg3Qwb-q7oc81xoswMwto88422y11wBz822weS4oaEnxO0Bo4O2-2l2UtwxwhU31w9O1lwlE-U2exi4UaEW4UmwsoqBwJK14xm1HzEjUlwhEe88o4qum7-2K0-obXCwLyESE2KwkQ0z8c84u2ubwHwNxe6Uak2-1vwxyo6O1FwgUjwOwWwjHDzUiwRK6E4-mEbUaU&__csr=iNI4keNk8fdkuBRsL7czFvdWblRQSysTFqtRnilaQOKAl5G9KqECHCFUDAjhqgzBogJuuKCaAjGcBzbKVFbALIx4cGaiABBBAz8GcLBQ4agFa5pFFUlVF8C9zF9uuaV-bzqGcK5UR5zoqyAbxFeWyokDCHDG5euV8OqVem9gVCjzEhDxuEGfyd7zoy4FEC26mXwDxGfG59-fUB1y6UF2oghUXGmAGxiqfAKUGeFGfyUWewFw8C6oGeKq4U4WawyyEOmuES9gyexG8yEb8G3iUKElwQUS2G4U-54eG8wJG5EdEc81Y80Pq0hOpa2fw2lE1n9FEbE5G0ZpoNyU4WqUkzU6m0oqbwSwhHiggximm0C8dU3RxK2aew1jm1dw3mO01hC0g9yAEKzo6e1-gnxna0Y80riw76wQw0kcax91kn402PU3pw3cU0ggg0WS440MFErw2i80B61Zw0xkx20u2fwvE0Gy11oS2p0Fzy01eVwi812o1H82Kw14Wu0j-0QE720lP8IU1e80N60478gw9h38apFEwxu5E0ZK0xm09QwMw2JE9o6d060w5mwCUa4pjwb-065E0mMy8Gp01eS4EZ1l0Fzy04jw2pogwf60-41ewuu4o2Gw&__comet_req=1&fb_dtsg={_dtsg}&jazoest=25479&lsd=UEIdUKYqlMER2LxiAXtnJt&__spin_r=1016820347&__spin_b=trunk&__spin_t=1727339339&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=useCometLocaleSelectorLanguageChangeMutation&variables=%7B%22locale%22%3A%22en_US%22%2C%22referrer%22%3A%22WWW_COMET_NAVBAR%22%2C%22fallback_locale%22%3Anull%7D&server_timestamps=true&doc_id=6451777188273168';

                fetch('https://www.facebook.com/api/graphql/', {{
                    method: 'POST',
                    headers: headers,
                    body: dataString,
                    credentials: 'include' // Important for using cookies in the request
                }})
                    .then(response => response.text())
                    .then(body => console.log(body))
                    .catch(error => console.error(error));
                """
                fetch = self.driver.execute_script(script)
                for _ in range(2):
                    self.driver.refresh()
                    sleep(1)


    # SEND CODE QR 
    def AutoSendQRCode(self):
        self.otp_qr_convert = Authentication(self.code) if self.code is not str() else str()
        self.arguments_scroll(2)
        for charOTP in self.otp_qr_convert:
            elm_auth = self.find_element(By.XPATH,'//input[@dir="ltr"]')
            if elm_auth is not None:
                elm_auth.send_keys(charOTP)
                self.TimeWriting()
        
        elm_auth.send_keys(Keys.ENTER)

        self.WaitByXpath('(//*[@role="none" and @data-visualcompletion="ignore"])[4]') # Wait Load
        self.arguments_click('(//*[@role="none" and @data-visualcompletion="ignore"])[4]') # Chọn Phương án Trust Device
    # Login với UID-PASSWORD
    def Login(self):
        if self.verify_login(): return # đã login
        
        if self.WaitByID("email"):
            # nhập username
            for charUser in self.c_user:
                elm_username = self.find_element(By.ID,"email")
                elm_username.send_keys(charUser)
                
                self.TimeWriting()
            
            # nhập password
            for charPassword in self.password:
                elm_password = self.find_element(By.ID , "pass")
                elm_password.send_keys(charPassword)
                self.TimeWriting()

            elm_password.send_keys(Keys.ENTER)      
            self.AntiSpam()  
            if "privacy_mutation" in self.driver.current_url:
                return 256281040558 # Kết quả mật khẩu không khớp
            elif "828281030927956" in self.driver.current_url:
                return 828281030927956 # Tài khoản bị khóa 
            # <input dir="ltr" autocomplete="off" aria-invalid="false" id=":r5:" class="x1i10hfl xggy1nq x1s07b3s x1a2a7pz xjbqb8w x1v8p93f xogb00i x16stqrj x1ftr3km x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xzsf02u x1vr9vpq x1iyjqo2 x1y44fgy x10d0gm4 x1fhayk4 x16wdlz0 x3cjxhe x8182xy xwrv7xz xeuugli xlyipyv x1hcrkkg xfvqz1d x12vv892 x163jz68 xpp3fsf xvr60a6 x1sfh74k x53uk0m x185fvkj x1p97g3g xmtqnhx x11ig0mb x1quw8ve xx0ingd x361rvq x10emqs4 xs8nzd4 x1fzehxr" type="text" value="" tabindex="0">
            elif "two_step_verification" in self.driver.current_url:

                if self.WaitByXpath('(//*[@dir="ltr" and @id=":r5:" and @value=""])'):
                    self.AutoSendQRCode() # TỰ ĐỘNG ĐIỀN QR CODE NẾU KHÔNG CÓ PHƯƠNG THỨC CHỜ THÔNG BÁO !
                else:
                    # CÓ PHƯƠNG THỨC DUYỆT THÔNG BÁO 
                    driver_ = self.find_element(By.XPATH,"(//*[@role='none' and @data-visualcompletion='ignore'])[1]")
                    if driver_:
                        self.arguments_click(driver_)
                        return self.Login()
                    
                    self.driver.implicitly_wait(3)
                    # Chọn xác minh 2FA

                    self.WaitByXpath('(//*[@role="none" and @data-visualcompletion="ignore"])[4]')

                    self.arguments_scroll(2)
                    self.arguments_click('(//*[@dir="auto"])[2]') # click vào Text

                    self.arguments_click('(//*[@role="none" and @data-visualcompletion="ignore"])[4]') # Chọn Phương án 2FA
                    # Xác nhận phương án
                    self.arguments_click("(//*[@role='none' and @data-visualcompletion='ignore'])[5]")

                    self.WaitByXpath('//input[@dir="ltr"]')

                    # TỰ ĐỘNG ĐIỀN QR CODE KHI ĐÃ CHỌN QR THÔNG BÁO

                    self.AutoSendQRCode()


                if self.otp_qr_convert == '': return 7749
                elif "828281030927956" in self.driver.current_url:
                    return 828281030927956 # Tài khoản bị khóa 
                
                self.verify_login()
                return
        else:
            self.driver.get('https://facebook.com')
        self.arguments_scroll(2)
                
        return self.Login() # lặp lại nếu lỗi

        




    ############################################################################
    # Kiểm tra và đợi các phần tử xuất hiện
    ############################################################################

    def arguments_scroll(self , number):
        sleep(1)
        y = random.choice([100,120,110,140])
        for _ in range(number):
            self.driver.execute_script(f"window.scrollBy(0, {y});")
            self.TimeWriting()
    def arguments_click(self, driver_):
        self.driver.implicitly_wait(random.randint(5,10))
        self.TimeWait()
        if type(driver_) is str:
            driver_ =  self.find_element(By.XPATH,driver_)

            if driver_ is None: return
        self.driver.execute_script(
                "arguments[0].click();",
                driver_) # click try Another

    def WaitByID(self,value):
        self.driver.implicitly_wait(10)
        try:
            WebDriverWait(self.driver , 60).until(
                EC.presence_of_all_elements_located((By.ID , value))
                )
                
            return 1
        except Exception as error:
            print(error)
            return 
    def WaitByName(self,value):
        self.driver.implicitly_wait(10)
        try:
            WebDriverWait(self.driver , 60).until(
                EC.presence_of_all_elements_located((By.NAME , value)))
            
            return 1
        except Exception as error:
            print(error)
            return
    
    def WaitByXpath(self,value):
        self.driver.implicitly_wait(10)
        try:
            WebDriverWait(self.driver , 60).until(
                EC.presence_of_all_elements_located((By.XPATH , value))
                )
            return 1
        except Exception as error:
            print(error)
            return
class Browser(QThread):
    signal = pyqtSignal(object)
    def __init__(self, objData):
        super(Browser,self).__init__()
        self.obj = objData
        self.driver = None
        self.report = {'msg':'Không xác định .','code': -1 , 'uid': self.obj['uid'] , 'date': ''}
    @property
    def config(self):
        if not hasattr(self, '_config'):
            self._config = json.loads(open(your_dir_config,'r',encoding='utf-8').read())
        return self._config
    
    def getDataFromSQL(self):
        global DEPOS_TEMP , NAMESQL

        nameSQL =  SubjectSQL.GetSQLTable(self)    
        for name in nameSQL:
            if name == 'ALL':continue
            depos = SQL(name).GetDataFromUID(self.obj['uid'])
            if depos != []:
                self.report.update({'SQL':name})
                DEPOS_TEMP , NAMESQL= depos[0], name

    def randomCardName(self):
        listCard = ["ANGLE (NVIDIA GeForce RTX 4090 Direct3D12 vs_6_0 ps_6_0, D3D12)",
            "ANGLE (AMD Radeon RX 7900 XTX Direct3D12 vs_6_0 ps_6_0, D3D12)",
            "ANGLE (NVIDIA Quadro RTX A6000 Direct3D12 vs_6_0 ps_6_0, D3D12)",
            "ANGLE (AMD Radeon Pro VII Direct3D12 vs_6_0 ps_6_0, D3D12)",
            "ANGLE (Intel Arc A770 Direct3D12 vs_6_0 ps_6_0, D3D12)",
            "ANGLE (NVIDIA GeForce RTX 4080 Vulkan 1.3, VK)",
            "ANGLE (AMD Radeon RX 7800 XT Vulkan 1.3, VK)",
            "ANGLE (NVIDIA Quadro RTX 5000 Vulkan 1.2, VK)",
            "ANGLE (AMD Radeon Pro W6800 Vulkan 1.2, VK)",
            "ANGLE (Intel Iris Xe Graphics Vulkan 1.2, VK)"]
        return random.choice(listCard)

    def sort_windows(self):

        try:
            x , y =  400 , 400
            x_position   =  self.obj['x_position']
            y_position   =  self.obj['y_position']

            self.driver.set_window_size(x, y)
            
            self.driver.set_window_position(x_position, y_position)
        except Exception as error:
            print(error)
            self.driver.quit()
            self.stop(self.obj['uid'])
    def ProfileProcess(self , uid):
        # Xóa thư mục Cache để giảm kích thước profile
        try:
            cache_dir = os.path.join(format(your_dir.joinpath('browser/profile/{}'.format(uid))), 'Default/Cache')
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
            
            # Xóa các thư mục không cần thiết khác nếu có
            other_dirs = ['Media Cache', 'IndexedDB', 'Local Storage', 'Application Cache']
            for dir_name in other_dirs:
                dir_path = os.path.join(your_dir, f"Default/{dir_name}")
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)
        except Exception as error:
            print("ProfileProcess" , error)


    def run(self):

        self.signal.emit(self.report)
        
        self.logging_dir  , _ = format(your_dir.joinpath('browser/profile/{}'.format(self.obj['uid']))) , self.ProfileProcess(self.obj['uid'])


        if self.isRunning():
            profile = profiles.Windows() # or .Android
            profile['cdp'].update({
                'maxtouchpoints':random.randint(4,10),
                'cores':random.choice([4,6,8,12,16,32]),  
            })
            profile['cdp']['useragent'].update({
                        'bitness':random.choice(['64','32']),
                        'architecture':random.choice(['x86','x64']),
                        'platform':random.choice(['Win32','Win64','MacIntel','Linux x86_64'])
                        })
            profile['cdp']['emulation'].update({
                        'width':400,
                        'height':400,
                        'deviceScaleFactor':0.8
                })
            options = webdriver.ChromeOptions()
            if self.config['config']['id.Profile']:
                options.add_argument('--user-data-dir={}'.format(self.logging_dir))
            options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1{random.randint(20,27)}.0.0.0 Safari/537.36')
            options.add_argument('--disable-signin-scoped-device-id')
            options.add_argument('--mute-audio')
            options.add_argument('--disable-gpu-shader-disk-cache')
            options.add_argument('--disable-application-cache')
            options.add_argument("--force-device-scale-factor=0.8")
            options.add_argument('--disable-bundled-ppapi-flash')
            options.add_argument('--disable-gaia-services')
            options.add_argument('--disable-gpu-compositing')
            options.add_argument('--disable-shared-workers')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-default-apps')
            options.add_argument('--disable-logging')
            options.add_argument('--allow-file-access-from-files')
            options.add_argument('--disable-gpu')
            options.add_argument('--use-fake-ui-for-media-stream')
            options.add_argument('--disable-blink-features')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-checking-optimization-guide-user-permissions')
            options.add_argument('--disable-shader-name-hashing')
            options.add_argument(f"--webgl-rerender={self.randomCardName()}")
            options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging', 'disable-popup-blocking'])
            options.add_argument('--disable-hid-detection-on-oobe')
            options.add_argument('--force-dev-mode-highlighting')
            options.add_argument("--force-webrtc-ip-handling-policy=disable_non_proxied_udp")
            options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns")
            options.add_argument('--ignore-certificate-errors-spki-list')
            options.add_argument('--ignore-ssl-errors')
            options.add_argument('--disable-webrtc-hw-encoding')
            options.add_argument('--no-sandbox')
            
            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "exit_type": "none",
                "exited_cleanly": True,
                'profile.default_content_setting_values': {'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                        'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                                                        'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                        'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                                                        'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                        'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
                                                        'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
                                                        'durable_storage': 2}
            }
            options.add_experimental_option('prefs', prefs)
            disable_options = [
                '--disable-background-networking',
                '--disable-client-side-phishing-detection',
                '--disable-webgl',
            ]
            for opt in disable_options:
                options.add_argument(opt)
            options.add_argument('--window-size=450,400')
            options.add_argument('--app=https://google.com')
            try:
                self.driver = Chrome(profile, options=options,
                    uc_driver=False
                    )
                self.sort_windows()
                sleep(2)
                self.driver.get("https://facebook.com")
            except Exception as error:
                return
        
            self.getDataFromSQL()
            tools = Facebook(self.driver , self.signal , self.report)
            keysMsg = tools.Login()
            tools.FeedisHome()
            self.report.update({'code':20032006,'content':str(datetime.now()),'id':self.report['uid'],'key':'message'})
            self.signal.emit(self.report)

    
    def stop(self):
        self.report.update({'code':20032006,'content':str(datetime.now()),'id':self.report['uid'],'key':'message'})
        self.signal.emit(self.report)
        try:
            self.driver.quit()
        except Exception:
            print("error")

        self.ProfileProcess(self.report['uid'])

        self.report.update({'code':99,'msg':''})

        self.signal.emit(self.report)
        self.terminate()
        self.quit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()
        self.ProfileProcess()