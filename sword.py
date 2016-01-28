import os
import re
import sys
import json
import sqlite3
import datetime
import requests
import configparser

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import robot
import qt.hotkey


def TerminateProc():
    os.system("TASKKILL /F /IM WuXia_Client.exe")
    os.system("TASKKILL /F /IM Client.exe")


def Login(rt, index):
    successed = False

    # Read config
    try:
        cp = configparser.ConfigParser()
        cp.read("c:/sword.conf")
        path = cp["Login"]["path"]
        user = cp["Login"]["user_{0}".format(index)]
        pwd = cp["Login"]["password_{0}".format(index)]
    except KeyError:
        return successed

    # start
    os.popen(path)

    # Sign in
    while not successed:
        hwnd = rt.findWindow("", "天涯明月刀登录程序")
        if hwnd:
            if rt.bind(hwnd, "normal", "normal", "normal", 0):
                rt.sleep(10000)
                if rt.findPic(0, 0, 1280, 720, "Login.bmp", "111111", 1.0, 0)[0] == -1:
                    rt.unbind()
                    rt.sleep(50000)
                    continue
                rt.leftClick(1010, 530)
                rt.sleep(15000)
                rt.keyPress(9)
                rt.sleep(100)
                [rt.keyPress(8) for i in range(20)]
                rt.sleep(100)
                rt.keyPressStr(user, 50)
                rt.sleep(100)
                rt.keyPress(9)
                rt.sleep(100)
                rt.keyPressStr(pwd, 50)
                rt.sleep(100)
                rt.leftClick(1000, 480)
                rt.sleep(5000)
                rt.leftClick(940, 250)  # Ad
                rt.sleep(5000)
                rt.leftClick(1000, 480)
                rt.sleep(5000)
                rt.leftClick(530, 475)
                rt.sleep(5000)
                rt.unbind()

                # Move reset
                rt.mouseMove(0, 0)
                rt.sleep(100)

                # Select role
                while not successed:
                    hwnd = rt.findWindow("GEMAINWINDOWCLASS", "")
                    if hwnd:
                        rt.sleep(30000)
                        rt.bind(hwnd, "dx2", "dx", "dx", 0)
                        rt.leftClick(1120, 620)
                        rt.unbind()
                        rt.sleep(10000)
                        successed = True
                    rt.sleep(1000)
        rt.sleep(1000)
    return successed


def ChangeRole(rt):
    # Quit to selecting page
    while True:
        while True:
            rt.keyPress(27)
            rt.sleep(1000)
            if rt.findPic(0, 0, 1280, 720, "Settings.bmp", "111111", 1.0, 0)[0] != -1:
                break
        rt.leftClick(640, 400)
        rt.sleep(1000)
        pic = rt.findPic(0, 0, 1280, 720, "BackToRolePage.bmp", "111111", 1.0, 0)
        if pic[0] != -1:
            rt.leftClick(pic[1], pic[2])
            rt.sleep(20000)
            break

    # Select next role
    rt.leftClick(90, 30)
    rt.sleep(1000)
    rt.leftClick(90, 30)
    rt.sleep(1000)
    rt.leftClick(1120, 620)
    rt.sleep(1000)
    rt.leftClick(1120, 620)
    rt.sleep(30000)


def ResetGameSettings(rt):
    # Open settings
    while True:
        rt.keyPress(27)
        rt.sleep(1000)
        if rt.findPic(0, 0, 1280, 720, "Settings.bmp", "111111", 1.0, 0)[0] != -1:
            break
    rt.leftClick(640, 300)
    rt.sleep(500)

    # Reset mode
    rt.leftClick(460, 230)
    rt.sleep(500)
    rt.leftClick(550, 190)
    rt.sleep(500)
    rt.leftClick(550, 300)
    rt.sleep(500)
    rt.leftClick(550, 190)
    rt.sleep(500)
    rt.leftClick(760, 560)
    rt.sleep(500)

    # Reset social
    rt.leftClick(455, 255)
    rt.sleep(500)
    rt.leftClick(455, 345)
    rt.sleep(500)
    rt.leftClick(596, 226)
    rt.sleep(500)
    rt.leftClick(760, 560)
    rt.sleep(500)

    # OK
    rt.leftClick(850, 560)
    rt.sleep(500)


class UnifiedExamination(robot.Task):

    def __init__(self):
        super(UnifiedExamination, self).__init__(self.doTasks)

    def doTasks(self):
        try:
            # Log
            logger = robot.Log("UnifiedExamination")

            # Step
            step = robot.Step()
            # step.goto(1)

            # Robot
            rt = robot.Robot()
            rt.setMouseDelay("dx", 1)
            rt.setKeypadDelay("dx", 1)
            rt.setPath("res")
            rt.setDict(0, "question.txt")
            rt.setMinRowGap(3)

            # Sqlite
            conn = sqlite3.connect("sword.db")
            cur = conn.cursor()

            accountIndex = 0
            roleChanged = False
            hwnd = 0
            while True:
                # Check connection
                if step.current() >= 2:
                    if rt.findPic(0, 0, 1280, 720, "Disconnect.bmp", "111111", 1.0, 0)[0] != -1:
                        logger.log("Disconnect")
                        # Restart
                        step.goto(0)

                # Steps
                if step.current() == 0:
                    # Login
                    TerminateProc()
                    if not Login(rt, accountIndex):
                        logger.log("Login failed")

                        # Flush log
                        logger.flush()

                        # Shut down computer
                        rt.exitOs(1)
                        break
                    else:
                        logger.log("Login successed")
                        step.next()
                elif step.current() == 1:
                    hwnd = rt.findWindow("GEMAINWINDOWCLASS", "")
                    if hwnd:
                        logger.log("Bind window: %d" % (hwnd))
                        rt.bind(hwnd, "dx2", "dx", "dx", 0)
                        step.next()
                    rt.sleep(1000)
                elif step.current() == 2:
                    # Reset settings
                    ResetGameSettings(rt)

                    # Hide others
                    rt.keyPress(17, 1)
                    rt.sleep(50)
                    rt.keyPress(80)
                    rt.sleep(50)
                    rt.keyPress(17, 0)
                    rt.sleep(50)

                    # Check if this role has done already
                    alreadyDone = False
                    rt.leftClick(1100, 80)
                    rt.sleep(1000)
                    rt.leftClick(1000, 275)
                    rt.sleep(1000)
                    rt.leftClick(350, 280)
                    rt.sleep(1000)
                    if rt.findPic(0, 0, 1280, 720, "CheckIn.bmp", "111111", 1.0, 0)[0] == -1:
                        alreadyDone = True
                    rt.keyPress(27)
                    rt.sleep(1000)
                    if alreadyDone:
                        logger.log("Already done")
                        step.goto(6)
                        continue
                    else:
                        logger.log("Not done")

                    # Switch chat channel
                    rt.keyPress(13)
                    rt.sendString(hwnd, "/j")
                    rt.keyPress(32)
                    rt.sleep(100)
                    rt.keyPress(27)

                    # Next step
                    step.next()
                    logger.log("Wait for asking")
                elif step.current() == 3:
                    # Wait for asking
                    pic = rt.findPic(30, 390, 60, 410, "QuestionIcon.bmp", "111111", 1.0, 0)
                    if pic[0] != -1:
                        # Click icon to show question
                        rt.leftClick(pic[1], pic[2])
                        rt.mouseMove(1, 1)
                        step.next()
                        logger.log("Wait for question showing")
                elif step.current() == 4:
                    # Wait for question
                    if rt.findPic(10, 360, 100, 400, "Question.bmp", "111111", 1.0, 0)[0] != -1:
                        step.next()
                elif step.current() == 5:
                    # Get question
                    words = rt.getWords(10, 360, 240, 440, "ffffff-808080", 0.95)
                    logger.log(words)
                    wordCount = rt.getWordCount(words)
                    if wordCount < 2:
                        step.goto(3)
                        continue
                    fragments = words.split("|")
                    del fragments[0:3]

                    # Search answer from local
                    finalAnswer = ""
                    keys = "%"
                    for key in fragments:
                        keys += key + "%"
                    cur.execute("Select question, answer from Questions where question like '{0}'".format(keys))
                    res = cur.fetchall()
                    if res:
                        minQuestionLen = 999
                        for r in res:
                            questionLen = len(re.sub("[_，。！？：；‘’“”《》]", "", r[0]))
                            if questionLen < minQuestionLen:
                                minQuestionLen = questionLen
                                finalAnswer = r[1]
                    else:
                        # Search answer from internet
                        fragments.sort(key=lambda x: len(x), reverse=True)
                        r = requests.get(
                            "http://huodong.duowan.com/wxdatiqi/backend/index.php",
                            params={"r": "index/GetQuestionByKeyword", "callback": "jsonpReturn", "keyword": fragments[0]})
                        if r.text != "jsonpReturn(null);":
                            text = r.text[13:-3]
                            text = text.replace("<font color=\\\"red\\\">", "")
                            text = text.replace("<\\/font>", "")
                            text = text.replace("},{", "},,,{")
                            answerList = text.split(",,,")
                            answerListCount = len(answerList)
                            if answerListCount == 0:
                                step.goto(3)
                                continue
                            elif answerListCount == 1:
                                j = json.loads(answerList[0])
                                finalAnswer = j["answer"]
                            else:
                                maxMatchCount = 1
                                minQuestionLen = 999
                                for answer in answerList:
                                    matchCount = 0
                                    j = json.loads(answer)
                                    question = j["question"]
                                    answer = j["answer"]
                                    for frag in fragments:
                                        if question.find(frag) != -1:
                                            matchCount += 1
                                    if matchCount > maxMatchCount:
                                        finalAnswer = j["answer"]
                                        maxMatchCount = matchCount
                                        minQuestionLen = len(
                                            re.sub("[_，。！？：；‘’“”《》]", "", question))
                                    elif matchCount == maxMatchCount:
                                        questionLen = len(
                                            re.sub("[_，。！？：；‘’“”《》]", "", question))
                                        if questionLen < minQuestionLen:
                                            finalAnswer = j["answer"]
                                            minQuestionLen = questionLen

                    # Send answer
                    if finalAnswer != "":
                        if len(finalAnswer) > 2:
                            rt.sleep(800, 0.2)
                        finalAnswer = "回答：" + finalAnswer
                        rt.keyPress(13)
                        rt.sendString(hwnd, finalAnswer)
                        rt.keyPress(13)
                    logger.log("Answer: %s" % (finalAnswer))

                    # Save
                    datetimeStr = datetime.datetime.now().strftime(
                        "%Y-%m-%d_%H-%M-%S")
                    bmpQuestion = datetimeStr + ".bmp"
                    rt.capture(10, 360, 240, 440, bmpQuestion)
                    # rt.sleep(800)
                    # bmpResult = datetimeStr + "_.bmp"
                    # rt.capture(10, 450, 380, 720, bmpResult)

                    # # Check result
                    # rt.sleep(120000)
                    # rt.leftClick(1250, 80)
                    # rt.sleep(1000)
                    # if rt.findPic(0, 0, 1280, 720, "Award.bmp", "111111", 0.9, 0)[0] != -1:
                    #     rt.leftClick(1250, 80)
                    #     rt.sleep(1000)
                    #     break

                    # Waiting for end
                    rt.sleep(240000)

                    # Mark
                    rt.sleep(1000)
                    rt.leftClick(1100, 80)
                    rt.sleep(1000)
                    rt.leftClick(1000, 275)
                    rt.sleep(1000)
                    rt.leftClick(600, 500)
                    rt.sleep(1000)
                    rt.keyPress(27)
                    rt.sleep(1000)

                    # Next step
                    step.next()
                elif step.current() == 6:
                    if roleChanged:
                        logger.log("Next account")
                        roleChanged = False
                        accountIndex += 1
                        step.goto(0)
                    else:
                        logger.log("Next role")
                        roleChanged = True
                        ChangeRole(rt)
                        step.goto(2)

                # Cpu
                rt.sleep(1)

        finally:
            rt.unbind()

            # Flush log
            logger.flush()
            logger.close()

            # Close sqlite
            cur.close()
            conn.commit()
            conn.close()


class Examination(robot.Task):

    def __init__(self):
        super(Examination, self).__init__(self.doTasks)

    def doTasks(self):
        rt = robot.Robot()
        try:
            # Log
            logger = robot.Log("Examination")

            # Step
            step = robot.Step()
            # step.goto(1)

            # Robot
            rt = robot.Robot()
            rt.setMouseDelay("dx", 1)
            rt.setKeypadDelay("dx", 1)
            rt.setPath("res")
            rt.setDict(0, "question.txt")
            rt.setMinRowGap(3)

            # Sqlite
            conn = sqlite3.connect("sword.db")
            cur = conn.cursor()

            # Loop
            while True:
                # Steps
                if step.current() == 0:
                    hwnd = rt.findWindow("GEMAINWINDOWCLASS", "")
                    if hwnd:
                        logger.log("Bind window: %d" % (hwnd))
                        rt.bind(hwnd, "dx2", "dx", "dx", 0)
                        step.next()
                        # step.goto(2)
                    rt.sleep(1000)
                elif step.current() == 1:
                    rt.leftClick(725, 475)
                    step.next()
                elif step.current() == 2:
                    if rt.findPic(0, 0, 1280, 720, "QnAStart.bmp", "111111", 1.0, 0)[0] != -1:
                        rt.sleep(100)
                        rt.leftClick(330, 530)
                        step.next()
                elif step.current() == 3:
                    done = False
                    pic = rt.findPic(465, 275, 505, 295, "QnAProgress.bmp", "111111", 1.0, 0)
                    if pic[0] != -1:
                        print("xy: %d, %d" % (pic[1], pic[2]))
                        matchCountIndex = 0

                        # Get question
                        words = rt.getWords(195, 295, 510, 370, "ffffff-808080", 0.95)
                        wordCount = rt.getWordCount(words)
                        if wordCount > 0:
                            fragments = words.split("|")
                            del fragments[0:2]
                            logger.log(fragments)

                            # Search answer from local
                            finalAnswer = ""
                            keys = "%"
                            for key in fragments:
                                keys += key + "%"
                            cur.execute("Select question, answer from Questions where question like '{0}'".format(keys))
                            curRes = cur.fetchall()
                            if curRes:
                                minQuestionLen = 999
                                for r in curRes:
                                    questionLen = len(re.sub("[_，。！？：；‘’“”《》]", "", r[0]))
                                    if questionLen < minQuestionLen:
                                        minQuestionLen = questionLen
                                        finalAnswer = r[1]
                                logger.log("Answer: %s" % (finalAnswer))

                                if finalAnswer != "":
                                    matchCountList = []
                                    for i in range(4):
                                        words = rt.getWords(218, 378 + i * 30, 480, 395 + i * 30, "ffffff-8599A5", 0.95)
                                        fragments = words.split("|")
                                        del fragments[0:2]
                                        logger.log(fragments)

                                        matchCount = 0
                                        for fragment in fragments:
                                            if finalAnswer.find(fragment) != -1:
                                                matchCount += 1
                                            else:
                                                matchCount = -1
                                                break
                                        matchCountList.append(matchCount)

                                maxMatchCount = max(matchCountList)
                                if matchCountList.count(maxMatchCount) == 1:
                                    matchCountIndex = matchCountList.index(maxMatchCount)

                                    # Selcet answer
                                    print("I: %d" % (matchCountIndex))
                                    rt.leftClick(350, 385 + matchCountIndex * 30)
                                    done = True

                        if not done:
                            # Can't select an answer then save the question
                            datetimeStr = datetime.datetime.now().strftime(
                                "%Y-%m-%d_%H-%M-%S")
                            bmpQuestion = "QnA_" + datetimeStr + "_Q.bmp"
                            rt.capture(195, 295, 510, 370, bmpQuestion)
                            bmpQuestion = "QnA_" + datetimeStr + "_A.bmp"
                            rt.capture(218, 378, 480, 485, bmpQuestion)

                            rt.sleep(100)

                            # No answer then avoid
                            logger.log("Unknown")
                            words = rt.getWords(218, 498, 480, 515, "ffffff-8599A5", 0.95)
                            wordCount = rt.getWordCount(words)
                            if wordCount > 0:
                                avoidAnswerStr = words.split("|")[2]
                                if avoidAnswerStr.find("本题") != -1:
                                    logger.log("Avoid")
                                    rt.leftClick(350, 505)
                                    done = True

                        if not done:
                            # No avoid chance then select a random answer
                            logger.log("Random")
                            rt.leftClick(350, 385 + matchCountIndex * 30)

                        # Waiting for changing
                        rt.isDisplayDead(470, 275, 520, 295, 5000)

                        # Reset mouse postion
                        rt.mouseMove(5, 5)
                        rt.sleep(10000)

                        if pic[1] == 471:
                            # This is the final quesstion
                            print("Esc")
                            rt.keyPress(27)
                            step.nextStep()
                elif step.current() == 4:
                    rt.sleep(1000)

                # Down cpu
                rt.sleep(1)
        finally:
            rt.unbind()

            # Flush log
            logger.flush()
            logger.close()

            # Close sqlite
            cur.close()
            conn.commit()
            conn.close()


class Drink(robot.Task):

    def __init__(self):
        super(Drink, self).__init__(self.doTasks)

    def doTasks(self):
        rt = robot.Robot()
        try:
            if rt.bind(rt.findWindowForeground(), "dx2", "dx", "dx", 0):
                rt.setPath("res")

                # Check time
                netTimeStr = rt.getWebTime()
                netTime = datetime.datetime.strptime(netTimeStr, "%Y-%m-%d %H:%M:%S")
                targetTime = netTime.replace(second=0)
                if (netTime.hour == 20 and netTime.minute > 45) or netTime.hour > 20:
                    targetTime = targetTime.replace(day=netTime.day + 1, hour=20, minute=45)
                else:
                    targetTime = targetTime.replace(hour=20, minute=45)
                rt.sleep((targetTime.timestamp() - netTime.timestamp()) * 1000, 0)

                while True:
                    pic = rt.findPic(
                        0, 0, 1280, 720, "Drink.bmp", "333333", 0.9, 0)
                    if pic[0] != -1:
                        rt.rightClick(pic[1], pic[2])
                        rt.sleep(50)
                        rt.mouseMove(1, 1)
                    rt.sleep(200)
        finally:
            rt.unbind()


# Systray
class MainWindow(QObject):

    """
    :type task: robot.Task
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.task = None

        # Add hot key

        self.hkStart = qt.hotkey.Hotkey(QKeySequence("F9"))
        self.hkStart.sActivate.connect(self.__start)
        self.hkStop = qt.hotkey.Hotkey(QKeySequence("F10"))
        self.hkStop.sActivate.connect(self.__stop)

        # System tray icon

        self.actGroup = QActionGroup(self)
        actUnifiedExamination = QAction("UnifiedExamination", self.actGroup)
        actPaint = QAction("Paint", self.actGroup)
        actDrink = QAction("Drink", self.actGroup)
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
        actUnifiedExamination.setChecked(True)

    def __start(self):
        if self.task is None and self.actGroup.checkedAction():
            if self.actGroup.checkedAction().text() == "UnifiedExamination":
                self.task = UnifiedExamination()
            elif self.actGroup.checkedAction().text() == "Paint":
                self.task = UnifiedExamination()
            elif self.actGroup.checkedAction().text() == "Drink":
                self.task = UnifiedExamination()
            else:
                return
            self.sysTray.showMessage(
                "Start", self.actGroup.checkedAction().text())
            self.sysTray.setIcon(QIcon("icon\on.png"))
            [x.setEnabled(False) for x in self.actGroup.actions()]
            self.task.start()

    def __stop(self):
        if self.task and self.actGroup.checkedAction():
            self.sysTray.showMessage(
                "Stop", self.actGroup.checkedAction().text())
            self.sysTray.setIcon(QIcon("icon\off.png"))
            [x.setEnabled(True) for x in self.actGroup.actions()]
            self.task.terminate()
            del self.task
            self.task = None


class Widget(QWidget):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.task = None

        # register button
        self.regBtn = QPushButton("Register")
        self.regBtn.clicked.connect(self.reg)

        # function box
        self.funcBox = QComboBox()
        self.funcBox.addItem("Fucntions")
        self.funcBox.addItem("Unified examination")
        self.funcBox.addItem("Examination")
        self.funcBox.addItem("Drink")
        self.funcBox.addItem("Learning tour")

        # Button layout
        btnHLayout = QHBoxLayout()
        btnHLayout.addWidget(self.regBtn)
        btnHLayout.addWidget(self.funcBox)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(btnHLayout)

        # Init widget
        self.setWindowTitle("DRK")
        self.setLayout(mainLayout)

        # Add hot key
        self.hkStart = qt.hotkey.Hotkey(QKeySequence("F9"))
        self.hkStart.sActivate.connect(self.__start)
        self.hkStop = qt.hotkey.Hotkey(QKeySequence("F10"))
        self.hkStop.sActivate.connect(self.__stop)

    def reg(self):
        rt = robot.Robot(True)
        rt.reg("FateCynff62bb4a6ec42e04e68567c3e009ec88", "Sword")
        self.regBtn.setEnabled(False)
        self.regBtn.setText("Registered")

    def __start(self):
        if self.task is None:
            if self.funcBox.currentIndex() == 1:
                self.task = UnifiedExamination()
            elif self.funcBox.currentIndex() == 2:
                self.task = Examination()
            elif self.funcBox.currentIndex() == 3:
                self.task = Drink()
            else:
                return
            self.task.start()
            self.funcBox.setEnabled(False)

    def __stop(self):
        if self.task:
            self.task.terminate()
            self.funcBox.setEnabled(True)
            del self.task
            self.task = None


if __name__ == "__main__":
    # # regist first
    # r = robot.Robot()
    # if r.reg("FateCynff62bb4a6ec42e04e68567c3e009ec88", "Sword") == 1:
    #     # Enter main loop
    #     a = QApplication(sys.argv)
    #     mainWindow = MainWindow()
    #     a.exec()
    a = QApplication(sys.argv)
    w = Widget()
    w.show()
    a.exec()
