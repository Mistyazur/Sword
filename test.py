import os
import re
import sys
import json
import sqlite3
import datetime
import requests
import configparser
import time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import robot
import qt.hotkey


class SocialQuestion(robot.Task):

    def __init__(self):
        super(SocialQuestion, self).__init__(self.doTasks)

    def __del__(self):
        print("123")

    def doTasks(self):
        try:
            rt = robot.Robot()
            print(1)
            for i in range(3):
                print(".")
                rt.sleep(1000)
            print(2)
        except SystemExit:
            print(3)
        finally:
            print(4)



# Systray
class MainWindow(QObject):

    """
    :type rt: robot.Task
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.rt = None
        self.stoped = True
        # Add hot key

        self.hkStart = qt.hotkey.Hotkey(QKeySequence("F9"))
        self.hkStart.sActivate.connect(self.__start)
        self.hkStop = qt.hotkey.Hotkey(QKeySequence("F10"))
        self.hkStop.sActivate.connect(self.__stop)

        # System tray icon

        self.actGroup = QActionGroup(self)
        actSocialQuestion = QAction("SocialQuestion", self.actGroup)
        self.actGroup.setExclusive(True)
        [x.setCheckable(True) for x in self.actGroup.actions()]
        menu = QMenu()
        menu.addActions(self.actGroup.actions())
        menu.addSeparator()
        menu.addAction("Quit", QApplication.quit)
        self.sysTray = QSystemTrayIcon(QIcon("icon\off.png"))
        self.sysTray.setContextMenu(menu)
        self.sysTray.show()

        # Set default checked
        actSocialQuestion.setChecked(True)

        # self.b =  SocialQuestion()
        # del self.b

    def __start(self):
        # self.b = SocialQuestion()
        # print(self.b)
        if self.stoped and self.actGroup.checkedAction():
            if self.rt:
                del self.rt
            if self.actGroup.checkedAction().text() == "SocialQuestion":
                self.rt = SocialQuestion()
            else:
                return
            self.sysTray.showMessage(
                "Start", self.actGroup.checkedAction().text())
            self.sysTray.setIcon(QIcon("icon\on.png"))
            [x.setEnabled(False) for x in self.actGroup.actions()]
            self.rt.start()
            self.stoped = False

    def __stop(self):
        if not self.stoped and self.actGroup.checkedAction():
            self.sysTray.showMessage(
                "Stop", self.actGroup.checkedAction().text())
            self.sysTray.setIcon(QIcon("icon\off.png"))
            [x.setEnabled(True) for x in self.actGroup.actions()]
            self.rt.terminate()
            self.stoped = True

def getRemoteTime():
    r = requests.get("https://www.baidu.com")
    gmtTimeStr = r.headers["Date"][5:-4]
    gmt = time.strptime(gmtTimeStr, "%d %b %Y %H:%M:%S")
    local = time.localtime(time.mktime(gmt)+8*60*60)
    localTimeStr = "%d-%02d-%02d %02d:%02d:%02d" % (local.tm_year, local.tm_mon, local.tm_mday, local.tm_hour, local.tm_min, local.tm_sec)
    print(localTimeStr)

if __name__ == "__main__":
    getRemoteTime()
    # r = robot.Robot()
    # if r.reg("FateCynff62bb4a6ec42e04e68567c3e009ec88", "Sword") == 1:
    #     # # Enter main loop
    #     a = QApplication(sys.argv)
    #     mainWindow = MainWindow()
    #     a.exec()
