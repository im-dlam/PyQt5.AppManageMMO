from main import *
from models import *
import pathlib
import os , json


your_dir_config  = pathlib.Path.cwd().joinpath("models/json/config.json")
your_dir = pathlib.Path.cwd()

class ShowConfig:
    def Config(self , widgets):
        filedumps = json.loads(open(your_dir_config,"r",encoding="utf-8").read())
        config = filedumps["config"]
        #######################################################################################
        # xử lý tỉ lệ
        widgets.TimeRun.setText(str(config["id.TimeWorking"])) # Time running
        widgets.LoopAct.setText(str(config["id.Loop"])) #  Loop
        widgets.likePercent.setText(str(config["id.PercentLike"])) #  Like feed
        widgets.ReadCommentPercent.setText(str(config["id.PercentReadComment"])) #  Read comment
        widgets.SharePercent.setText(str(config["id.PercentShare"])) # share 
        widgets.CommentPercent.setText(str(config["id.PercentComment"])) # commet 
        widgets.JoinGroupPercent.setText(str(config["id.PercentJoinGroup"])) # join group
        widgets.StoryPercent.setText(str(config["id.PercentViewStory"])) # vew story
        widgets.ReelPercent.setText(str(config["id.PercentViewReel"])) # view reel
        widgets.ReadReelCommentPercent.setText(str(config["id.PercentViewCommentReel"])) # read comment reel
        widgets.ViewNotificationsPercent.setText(str(config["id.PercentViewNotications"])) # read notifi
        widgets.ViewFeedAdminPostPercent.setText(str(config["id.PercentViewFeedAdmin"])) # view feed admin post
        widgets.AddFriendsPercent.setText(str(config["id.PercentAddFriendNew"])) # add friends
        widgets.StoryPostsPercent.setText(str(config["id.PercentPostsStory"])) # post story

        idText = "\n".join(config["id.IDUser"]) if isinstance(config["id.IDUser"], list) else config["id.IDUser"]
        GroupText = "\n".join(config["id.IDGroup"]) if isinstance(config["id.IDGroup"], list) else config["id.IDUser"]
        CommentText = "\n".join(config["id.Text"]) if isinstance(config["id.Text"], list) else config["id.IDUser"]

        widgets.plainID.setPlainText(idText)
        widgets.plainGroup.setPlainText(GroupText)
        widgets.plainText.setPlainText(CommentText)
        widgets.ApiSheet.setText(config["id.SheetApi"])
class ConfigProxy:
    def ProxyClear(self):
        filedumps =  json.loads(open(your_dir_config,"r",encoding="utf-8").read())
        filedumps["proxy"]["list"] =  []
        with open(your_dir_config , "w" , encoding="utf-8") as log_:
            json.dump(
                filedumps,
                log_,
                ensure_ascii=0,
                indent=4)
    
    def ProxyAdd(self, proxyPlainText : str):
        filedumps =  json.loads(open(your_dir_config,"r",encoding="utf-8").read())
        filedumps["proxy"]["list"] =  proxyPlainText
        with open(your_dir_config , "w" , encoding="utf-8") as log_:
            json.dump(
                filedumps,
                log_,
                ensure_ascii=0,
                indent=4)
class ConfigUser:
    def __init__(self , widgets) :
        self.your_dir  = pathlib.Path.cwd().joinpath("models/json/config.json")
        self.filedumps = None
        self.widgets   =  widgets

        self.setconfig()
        self.logfile()

    def fileConfig(self):
        
        with open(self.your_dir,"r",encoding="utf-8") as r:
            return r.read()
    
    def setconfig(self):

        self.filedumps =  json.loads(self.fileConfig())

        ConfigUpdate = {
            "id.TimeWorking":       int(self.widgets.TimeRun.text()),
            "id.Loop":              int(self.widgets.LoopAct.text()),

            ########################################################################################
            # "id.Profile": False,        #
            # "id.Backup": True,          #
            # "id.Proxy": False,          #
            # "id.Proxyauto": False,      #   => Phần này chuyển qua Ui_functions.py tự động cập nhật file json khi người dùng chuyển đổi
            # "id.BrowserAuto":True,      #
            # "id.BrowserOptimize":True,  #
            # "id.chatgpt":True,          #
            # "id.BrowserHeadless":False, #
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

            "id.SheetApi": self.widgets.ApiSheet.text() if self.widgets.StoryPostsPercent.text()  != "" else "147SpHvtiMrbMt2RCvPh80G4eWpHusSsxmFRyPrA7h8Y",

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

