from main import *
from selenium import webdriver



class Browser(QThread):
    signal = pyqtSignal(object)
    def __init__(self, objData):
        super(Browser,self).__init__()
        self.obj = objData
        self.driver = None

    def sort_windows(self):
        x , y =  350 , 400
        number =  self.obj['number']
        max_width   =  self.obj['max_width']
        max_heigh   =  self.obj['max_height']

        self.driver.set_window_size(x, y)
        x_position = (number % max_width) * x
        y_position = 0
        if number % max_width == 0 and number != 0:
            y_position += (y + 10)
        self.driver.set_window_position(x_position, y_position)
    def run(self):
        
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--app=https://google.com')
        self.driver = webdriver.Chrome(options=self.options)
        self.sort_windows()
        self.driver.get("https://fb.com")

        import time
        time.sleep(1000)
