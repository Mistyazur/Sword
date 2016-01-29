import os
import io
import time
import random
import ctypes
import requests
import threading
import pythoncom
import win32com.client
import PIL.Image
import logging
import logging.handlers

__all__ = ["Robot", "Log", "Task", "Step"]

__version__ = "1.0.0"


class Robot(object):

    def __init__(self, reg=False):
        super(Robot, self).__init__()

        if reg:
            # Load reg dll
            regDll = ctypes.windll.LoadLibrary("DmReg.dll")
            regDll.SetDllPathW("dm.dll", 0)

        # Load dm plugin
        pythoncom.CoInitialize()
        self.dm = win32com.client.Dispatch('dm.dmsoft')
        pythoncom.CoUninitialize

    ################################################################
    # Base
    ################################################################

    def reg(self, code, info):
        if self.dm.Ver() == '3.1232':
            return 1
        else:
            return self.dm.Reg(code, info)

    def setPath(self, dirname):
        path = os.path.join(os.getcwd(), dirname)
        return self.dm.SetPath(path)

    def setSimMode(self, mode):
        return self.dm.SetSimMode(mode)

    def setDisplayInput(self, mode):
        return self.dm.SetDisplayInput(mode)

    ################################################################
    # System
    ################################################################

    # Log off 0
    # Shut down 1
    # Restart 2
    def exitOs(self, t):
        return self.dm.ExitOs(t)

    def beep(self):
        return self.dm.Beep(1000, 1000)

    def sleep(self, msec, delta=0.1):
        random_msec = int(random.uniform(msec * (1 - delta), msec * (1 + delta)))
        c = random_msec // 100
        for i in range(c):
            time.sleep(0.1)
        time.sleep(random_msec % 100 / 1000)

    def getNtpTime(self):
        return self.dm.GetNetTimeByIp("cn.ntp.org.cn|tw.ntp.org.cn")

    def getWebTime(self):
        r = requests.get("https://www.baidu.com")
        gmtTimeStr = r.headers["Date"][5:-4]
        gmt = time.strptime(gmtTimeStr, "%d %b %Y %H:%M:%S")
        local = time.localtime(time.mktime(gmt)+8*60*60)
        localTimeStr = "%d-%02d-%02d %02d:%02d:%02d" % (local.tm_year, local.tm_mon, local.tm_mday, local.tm_hour, local.tm_min, local.tm_sec)
        return localTimeStr

    ################################################################
    # Window
    ################################################################

    def enumWindow(self, parent, title, classname, filterf):
        return self.dm.EnumWindow(parent, title, classname, filterf)

    def findWindow(self, classname, title):
        return self.dm.FindWindow(classname, title)

    def findWindowForeground(self):
        return self.dm.GetForegroundWindow()

    def bind(self, hwnd, display, mouse, keypad, mode):
        return self.dm.BindWindow(hwnd, display, mouse, keypad, mode)

    def unbind(self):
        return self.dm.UnBindWindow()

    def getBindWindow(self):
        return self.dm.GetBindWindow()

    def sendString(self, hwnd, sendStr):
        return self.dm.SendString(hwnd, sendStr)

    ################################################################
    # Display
    ################################################################

    def isDisplayDead(self, x1, y1, x2, y2, t):
        return self.dm.IsDisplayDead(x1, y1, x2, y2, t)

    def capture(self, x1, y1, x2, y2, name):
        return self.dm.Capture(x1, y1, x2, y2, name)

    def captureImage(self, x1, y1, x2, y2):
        info = self.dm.GetScreenDataBmp(x1, y1, x2, y2)
        if info[0]:
            data = ctypes.string_at(info[1], info[2])
            dataIo = io.BytesIO(data)
            image = PIL.Image.open(dataIo)
            return image
        return None

    def setDisplayInputImage(self, image):
        dataIo = io.BytesIO()
        image.save(dataIo, "BMP")
        data = ctypes.create_string_buffer(dataIo.getvalue())
        return self.dm.SetDisplayInput("mem:%d,%d" % (ctypes.addressof(data), ctypes.sizeof(data)))

    def resetDisplayInput(self):
        self.dm.SetDisplayInput("screen")

    def getScreenBmp(self, x1, y1, x2, y2):
        return self.dm.GetScreenDataBmp(x1, y1, x2, y2)

    def getColor(self, x, y):
        return self.dm.GetColor(x, y)

    def findPic(self, x1, y1, x2, y2, picname, deltacolor, sim, direct):
        return self.dm.FindPic(x1, y1, x2, y2, picname, deltacolor, sim, direct)

    ################################################################
    # Ocr
    ################################################################

    def setDict(self, index, filename):
        return self.dm.SetDict(index, filename)

    def setMinRowGap(self, gap):
        return self.dm.SetMinRowGap(gap)

    def ocr(self, x1, y1, x2, y2, colorformat, sim):
        return self.dm.Ocr(x1, y1, x2, y2, colorformat, sim)

    def getWords(self, x1, y1, x2, y2, colorformat, sim):
        return self.dm.GetWords(x1, y1, x2, y2, colorformat, sim)

    def getWordCount(self, words):
        return self.dm.GetWordResultCount(words)

    def getWordPos(self, words, index):
        return self.dm.GetWordResultPos(words, index)

    def getWordStr(self, words, index):
        return self.dm.GetWordResultStr(words, index)

    ################################################################
    # Mouse
    ################################################################

    def setMouseDelay(self, t, d):
        return self.dm.SetMouseDelay(t, d)

    def getCursorPos(self):
        return self.dm.GetCursorPos()

    def mouseMove(self, x, y):
        self.dm.MoveTo(x, y)

    ################################################################
    # Keypad
    ################################################################

    def setKeypadDelay(self, t, d):
        return self.dm.SetKeypadDelay(t, d)

    def leftClick(self, x=0, y=0):
        if x != 0 or y != 0:
            self.dm.MoveTo(x, y)
        self.dm.LeftClick()

    def leftDClick(self, x=0, y=0):
        if x != 0 or y != 0:
            self.dm.MoveTo(x, y)
        self.dm.LeftDoubleClick()

    def rightClick(self, x=0, y=0):
        if x != 0 or y != 0:
            self.dm.MoveTo(x, y)
        self.dm.RightClick()

    def keyPress(self, key, downup=2):
        if (downup == 0):
            self.dm.KeyUp(key)
        elif (downup == 1):
            self.dm.KeyDown(key)
        else:
            self.dm.KeyPress(key)

    def keyPressStr(self, s, delay):
        return self.dm.KeyPressStr(s, delay)

    def waitKey(self, keycode, timeout=0):
        return self.dm.WaitKey(keycode, timeout)

    def getKeyState(self, keycode):
        return self.dm.GetKeyState(keycode)


class Log(object):

    def __init__(self, logname):
        super(Log, self).__init__()

        # Init log handle
        # formatter = logging.Formatter(
        #     "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
        formatter = logging.Formatter("[%(asctime)s] %(message)s")
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.ch.setFormatter(formatter)

        self.fh = logging.FileHandler(os.path.join(logname + ".log"))
        self.fh.setLevel(logging.DEBUG)
        self.fh.setFormatter(formatter)

        self.mh = logging.handlers.MemoryHandler(
            4096, logging.WARNING, self.fh)

        # Init logger
        self.logger = logging.getLogger(logname)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.ch)
        self.logger.addHandler(self.mh)

    def close(self):
        self.logger.removeHandler(self.ch)
        self.logger.removeHandler(self.mh)

    def log(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def flush(self):
        self.logger.warning("================================")
        # super(MemoryHandler, self.mh).flush()


class Task(threading.Thread):

    def __init__(self, todo):
        super(Task, self).__init__()
        self.todo = todo

    def __asyncRaise(self, tid, exctype):
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("Invalid thread id")
        elif res != 1:
            # If it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def run(self):
        # try:
            self.todo()
        # except SystemExit:
        #     print("SystemExit")
        # finally:
        #     print("Finally")

    def terminate(self):
        if self.isAlive():
            for tid, tobj in threading._active.items():
                if tobj is self:
                    self.__asyncRaise(tid, SystemExit)
                    return


class Step(object):

    def __init__(self):
        super(Step, self).__init__()
        self.__curStep = 0

    def current(self):
        return self.__curStep

    def goto(self, stepNumber):
        self.__curStep = stepNumber

    def prev(self):
        if self.__curStep > 0:
            self.__curStep -= 1

    def next(self):
        self.__curStep += 1
