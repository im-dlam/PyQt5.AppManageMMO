from main import *
from models import *
import pathlib
import os , json
class ConfigUser:
    def __init__(self) :
        self.your_dir = pathlib.Path.cwd().joinpath("models/json/config.json")

    def fileConfig(self):
        
        with open(self.your_dir,"r",encoding="utf-8") as r:
            return r.read()
    
    def setconfig(self):

        self.filedumps =  json.loads(self.fileConfig())

        print(self.filedumps)

