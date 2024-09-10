from main import *
from . Pyotp import *
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

DEPOS_TEMP , QHD = () ,  0

class Facebook:
    def __init__(self, driver: WebDriver):
        global DEPOS_TEMP , QHD
        self.driver = driver
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


        
    def verify_login(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@class='MAWOembedIframe']"))
            )
            return 1
        except:
            return 0

    def Notifications(self):
        try:
            for _ in range(2):
                self.driver.implicitly_wait(10)
                element_nofi = self.driver.find_element(By.XPATH, "(//*[@aria-label='Notifications'])[1]")
                if element_nofi.is_displayed():
                    element_nofi.click()
                    sleep(2)
        except Exception as e:
            print(e)
    
    def Messengers(self):
        try:
            for loop in range(2):
                self.driver.implicitly_wait(10)
                element_nofi = self.driver.find_element(By.XPATH,"(//*[@aria-label='Messenger'])[1]")

                self.arguments_click(element_nofi)
                sleep(3)
        except Exception as error:
            print(error)
    
    def SeeMorePosts(self):
        try:
            element_show_more = self.driver.find_element(By.XPATH,'//div[text()="See more"]')

            self.arguments_click(element_show_more)
        except Exception as error:
            print(error)


    def CommentRead(self):
        try:
            element_comment = self.driver.find_element(By.XPATH,'//span[text()="Comment"]')

            self.arguments_click(element_comment)

            self.SeeMorePosts()
            self.closeButtonElement()
        except Exception as error:
            print("CommentRead" , error)

    
    def closeButtonElement(self):
        self.driver.implicitly_wait(10)
        try:
            element_commentButton = self.driver.find_element(By.XPATH,"//*[@aria-label='Close']")
            # self.driver.execute_script('arguments[0].click();',element_commentButton)

        
            self.arguments_click(element_commentButton)
        except Exception as error:
            print("closeButtonElement",error)
        
    def ActionReactions(self):
        keyID = {
            0 : 'Like',
            30: 'Love',
            60: 'Haha',
            90: 'Care'
        }
        idRandom = random.choice([0,30,60,90])
        self.driver.implicitly_wait(10)



        try:
            element_textLike =  self.driver.find_element(By.XPATH,'//span[text()="Like"]')

            ActionChains(self.driver).click_and_hold(element_textLike).perform() # giữ chuột
            
            sleep(1)

            ActionChains(self.driver).move_to_element_with_offset(element_textLike,idRandom,-30).click().perform()

            return keyID[idRandom]
        except Exception as error:
            print("ActionReactions",error)
    
    def FeedisHome(self):
        person , check , ifp = [4,8,12,16,18,22] , 0 , 4
        timeWork =  datetime.now() + timedelta(minutes=self.config['config']['id.TimeWorking'])
        x_position_scroll , loop_add = 0 , 0
        while datetime.now() <= timeWork:
            loop_add += 1


            # ti le likex
            if check:
                ifp = random.choice(person)
                check  = 0

            # thuc hien hanh dong
            if loop_add % ifp == 0:
                self.ActionReactions()
                self.CommentRead()

                try:
                    random.choice([self.Messengers , self.Notifications ] + [None] * 5)()
                except Exception as error:
                    print("FeedisHome" ,error)

                self.closeButtonElement()
                check = 1

                sleep(random.randint(4,7))
            
            # keo cuon web
            x_position_scroll += random.randint(110,200)
            self.driver.execute_script(f"window.scrollTo(0, {x_position_scroll});")
            self.TimeWriting()

            continue

    # Login với UID-PASSWORD
    def Login(self):
        if self.verify_login(): return # đã login

        if self.WaitByID("email"):
            # nhập username
            for charUser in self.c_user:
                elm_username = self.driver.find_element(By.ID,"email")
                elm_username.send_keys(charUser)
                
                self.TimeWriting()
            
            # nhập password
            for charPassword in self.password:
                elm_password = self.driver.find_element(By.ID , "pass")
                elm_password.send_keys(charPassword)
                self.TimeWriting()

            elm_password.send_keys(Keys.ENTER)        
            if "privacy_mutation" in self.driver.current_url:
                return 256281040558 # Kết quả mật khẩu không khớp
            elif "828281030927956" in self.driver.current_url:
                return 828281030927956 # Tài khoản bị khóa 
            
            elif "two_step_verification" in self.driver.current_url:
                # Next two_factor
                self.arguments_click("(//*[@role='none' and @data-visualcompletion='ignore'])[1]")
                self.driver.implicitly_wait(3)
                # Chọn xác minh 2FA

                self.WaitByXpath('(//*[@role="none" and @data-visualcompletion="ignore"])[4]')

                self.arguments_scroll(2)
                self.arguments_click('(//*[@dir="auto"])[2]') # click vào Text

                self.arguments_click('(//*[@role="none" and @data-visualcompletion="ignore"])[4]') # Chọn Phương án 2FA
                # Xác nhận phương án
                self.arguments_click("(//*[@role='none' and @data-visualcompletion='ignore'])[5]")

                self.WaitByXpath('//input[@dir="ltr"]')

                current_otp = Authentication(self.code) if self.code != "" else ""
                self.arguments_scroll(2)
                for charOTP in current_otp:
                    elm_auth = self.driver.find_element(By.XPATH,'//input[@dir="ltr"]')
                    elm_auth.send_keys(charOTP)
                    self.TimeWriting()
                elm_auth.send_keys(Keys.ENTER)

                self.WaitByXpath('(//*[@role="none" and @data-visualcompletion="ignore"])[4]') # Wait Load
                self.arguments_click('(//*[@role="none" and @data-visualcompletion="ignore"])[4]') # Chọn Phương án Trust Device

                if current_otp == '': return 7749
                elif "828281030927956" in self.driver.current_url:
                    return 828281030927956 # Tài khoản bị khóa 
                
                self.verify_login()
                return
            self.arguments_scroll(2)
                
        return self.Login() # lặp lại nếu lỗi

        




    ############################################################################
    # Kiểm tra và đợi các phần tử xuất hiện
    ############################################################################

    def arguments_scroll(self , number):
        sleep(1)
        for _ in range(number):
            self.driver.execute_script("window.scrollBy(0, 100);")
            self.TimeWriting()
    def arguments_click(self, xpath_elm):
        self.driver.implicitly_wait(random.randint(5,10))
        self.TimeWait()
        self.driver.execute_script(
            "arguments[0].click();",
            self.driver.find_element(By.XPATH,xpath_elm)) # click try Another

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
        global DEPOS_TEMP

        nameSQL =  SubjectSQL.GetSQLTable(self)    
        for name in nameSQL:
            if name == 'ALL':continue
            depos = SQL(name).GetDataFromUID(self.obj['uid'])
            if depos != []:
                self.report.update({'SQL':name})
                DEPOS_TEMP = depos[0]

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
            x , y =  350 , 400
            x_position   =  self.obj['x_position']
            y_position   =  self.obj['y_position']

            self.driver.set_window_size(x, y)
            
            self.driver.set_window_position(x_position, y_position)
        except Exception as error:
            print(error)
            self.driver.quit()
            self.stop()
    def ProfileProcess(self):
        # Xóa thư mục Cache để giảm kích thước profile
        try:
            cache_dir = os.path.join(self.logging_dir, 'Default/Cache')
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
            
            # Xóa các thư mục không cần thiết khác nếu có
            other_dirs = ['Media Cache', 'IndexedDB', 'Local Storage', 'Application Cache']
            for dir_name in other_dirs:
                dir_path = os.path.join(self.logging_dir, f"Default/{dir_name}")
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)
        except Exception as error:
            print("ProfileProcess" , error)


    def run(self):

        self.signal.emit(self.report)
        
        self.logging_dir  , _ = format(your_dir.joinpath('browser/profile/{}'.format(self.obj['uid']))) , self.ProfileProcess()

        
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
                        'width':350,
                        'height':400,
                        'deviceScaleFactor':0.6
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
            options.add_argument('--window-size=300,400')
            options.add_argument('--app=https://google.com')
            try:
                self.driver = Chrome(profile, options=options,
                    uc_driver=False
                    )
                self.sort_windows()
                sleep(2)
                self.driver.get("https://facebook.com")
            except Exception as error:
                print(error)
                return
            self.getDataFromSQL()
            tools = Facebook(self.driver)
            keysMsg = tools.Login()
            tools.FeedisHome()
            self.report.update({'code':keysMsg})
            self.signal.emit(self.report)

    
    def stop(self):

        self.report.update({'code':99,'msg':'close...'})
        try:
            self.driver.quit()
        except Exception:
            print("error")

        self.ProfileProcess()

        self.report.update({'code':99,'msg':''})
        self.terminate()
        self.quit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()
        self.ProfileProcess()