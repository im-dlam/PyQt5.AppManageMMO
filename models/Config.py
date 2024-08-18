from main import *
from models import *
import pathlib
import os , json
class ConfigUser:
    def __init__(self , widgets) :
        self.your_dir  = pathlib.Path.cwd().joinpath("models/json/config.json")
        self.filedumps = None
        self.widgets   =  widgets
        self.setconfig()


    def fileConfig(self):
        
        with open(self.your_dir,"r",encoding="utf-8") as r:
            return r.read()
    
    def setconfig(self):

        self.filedumps =  json.loads(self.fileConfig())

        ConfigUpdate = {
            "id.TimeWorking":       int(self.widgets.TimeRun.text()),
            "id.Loop":              int(self.widgets.LoopAct.text()),

            ########################################################################################
            "id.Profile": False,
            "id.Backup": True,
            "id.Proxy": False,
            "id.Proxyauto": False,
            "id.BrowserAuto":True,
            "id.BrowserOptimize":True,
            "id.chatgpt":True,
            "id.BrowserHeadless":False,
            ########################################################################################
            "id.PercentLike": int(self.widgets.likePercent.text()),
            "id.PercentReadComment": int(self.widgets.ReadCommentPercent.text()),
            "id.PercentShare": int(self.widgets.SharePercent.text()),
            "id.PercentComment": int(self.widgets.CommentPercent.text()),
            "id.PercentJoinGroup": int(self.widgets.JoinGroupPercent.text()),
            "id.PercentViewStory": int(self.widgets.StoryPercent.text()),
            "id.PercentViewReel": int(self.widgets.ReelPercent.text()),

            "id.PercentViewCommentReel": int(self.widgets.ReadReelCommentPercent.text()),
            "id.PercentViewNotications": int(self.widgets.ViewNotificationsPercent.text()),
            "id.PercentViewFeedAdmin": int(self.widgets.ViewFeedAdminPostPercent.text()),
            "id.PercentAddFriendNew": int(self.widgets.AddFriendsPercent.text()),
            "id.PercentPostsStory": int(self.widgets.StoryPostsPercent.text()),


            ########################################################################################

            "id.SheetApi": self.widgets.StoryPostsPercent.text() if self.widgets.StoryPostsPercent.text()  != "" else "147SpHvtiMrbMt2RCvPh80G4eWpHusSsxmFRyPrA7h8Y",

            ########################################################################################
            "id.IDUser": [value.strip("\n") for value in self.widgets.plainID.toPlainText().split("\n")],
            "id.IDGroup": [value.strip("\n") for value in self.widgets.plainGroup.toPlainText().split("\n")],
            "id.Text": [value.strip("\n") for value in self.widgets.plainText.toPlainText().split("\n")]
        }
        self.filedumps['config'].update(ConfigUpdate)
    def logfile(self):
        with open(self.your_dir , "w" , encoding="utf-8") as log_:
            json.dump(
                self.filedumps,
                log_,
                ensure_ascii=0,
                indent=4)

