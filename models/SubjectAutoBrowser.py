from main import *
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


DEPOS_TEMP , QHD = () ,  0
keys = {
    256281040558: 'account no login ! error password .'
}
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

    def TimeWriting(self):
        sleep(float(random.randrange(1,10)/30))



    def Login(self):
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

            self.driver.implicitly_wait(3)
            elm_password.send_keys(Keys.ENTER)        
            self.driver.implicitly_wait(5)
            print(self.driver.current_url)
            if "privacy_mutation" in self.driver.current_url:
                return 256281040558 # Kết quả mật khẩu không khớp
            
            
        
        return self.Login() # lặp lại nếu lỗi

        




    ############################################################################
    # Kiểm tra và đợi các phần tử xuất hiện
    ############################################################################

    
    def WaitByID(self,value):
        try:
            print("ok")
            WebDriverWait(self.driver , 60).until((EC.presence_of_all_elements_located((By.ID , value))))
            return 1
        except Exception as error:
            print(error)
            return 
    def WaitByName(self,value):
        try:
            WebDriverWait(self.driver , 60).until((EC.presence_of_all_elements_located((By.NAME , value))))
            return 1
        except Exception as error:
            print(error)
            return
    
    def WaitByXpath(self,value):
        try:
            WebDriverWait(self.driver , 60).until((EC.presence_of_all_elements_located((By.XPATH , value))))
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
        self.report = {'msg':'Không xác định .','code': 0 , 'uid': 0 , 'date': ''}
    def getDataFromSQL(self):
        global DEPOS_TEMP

        nameSQL =  SubjectSQL.GetSQLTable(self)    
        for name in nameSQL:
            if name == 'ALL':continue
            depos = SQL(name).GetDataFromUID(self.obj['uid'])
            if depos != []: DEPOS_TEMP = depos[0]

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
    
    def run(self):
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
                import time
                time.sleep(2)
                self.driver.get("https://facebook.com")
            except Exception as error:
                print(error)
                return
            self.getDataFromSQL()
            tools = Facebook(self.driver)
            tools.Login()
            time.sleep(1000)

    
    def stop(self):
        try:
            self.driver.quit()
        except Exception:
            print("error")
        self.terminate()
        self.quit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()