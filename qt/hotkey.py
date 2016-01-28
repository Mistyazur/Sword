import ctypes
import win32con
import win32api
import ctypes.wintypes

from PyQt5.QtCore import *
from PyQt5.QtGui import *

User32 = ctypes.windll.user32
InstanceCount = 0


class HotkeyCenter(QAbstractNativeEventFilter):

    hotkeys = {}

    def __init__(self):
        global InstanceCount
        super(HotkeyCenter, self).__init__()
        if not InstanceCount:
            QAbstractEventDispatcher.instance().installNativeEventFilter(self)
        InstanceCount += 1

    def __del__(self):
        global InstanceCount
        InstanceCount -= 1
        if not InstanceCount:
            try:
                QAbstractEventDispatcher.instance().removeNativeEventFilter(
                    self)
            except AttributeError:
                pass

    def nativeEventFilter(self, eventType, message):
        if eventType == 'windows_generic_MSG':
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            if msg.message == win32con.WM_HOTKEY:
                keycode = win32api.HIWORD(msg.lParam)
                modifiers = win32api.LOWORD(msg.lParam)
                self.activeHotkey(keycode, modifiers)
        return False, 0

    def addHotkey(self, nativeKey, nativeMods, hotkey):
        if (nativeKey, nativeMods) in self.hotkeys:
            return False
        self.hotkeys[(nativeKey, nativeMods)] = hotkey
        return True

    def delHotkey(self, nativeKey, nativeMods):
        if (nativeKey, nativeMods) in self.hotkeys:
            self.hotkeys.pop((nativeKey, nativeMods))
            return True
        return False

    def activeHotkey(self, nativeKey, nativeMods):
        hotkey = self.hotkeys.get((nativeKey, nativeMods))
        if hotkey:
            hotkey.sActivate.emit()


class Hotkey(QObject):

    sActivate = pyqtSignal()

    def __init__(self, hotkey):
        super(Hotkey, self).__init__()
        self.hotkey = hotkey
        self.exist = False
        self.hotkeyCenter = HotkeyCenter()
        self.__setHotkey()

    def __nativeModifiers(self, modifiers):
        native = 0
        if (modifiers & Qt.ShiftModifier):
            native |= win32con.MOD_SHIFT
        if (modifiers & Qt.ControlModifier):
            native |= win32con.MOD_CONTROL
        if (modifiers & Qt.AltModifier):
            native |= win32con.MOD_ALT
        if (modifiers & Qt.MetaModifier):
            native |= win32con.MOD_WIN
        return native

    def __nativeKeycode(self, key):
        if key == Qt.Key_Escape:
            return win32con.VK_ESCAPE
        elif key == Qt.Key_Tab:
            return win32con.VK_TAB
        elif key == Qt.Key_Backtab:
            return win32con.VK_TAB
        elif key == Qt.Key_Backspace:
            return win32con.VK_BACK
        elif key == Qt.Key_Return:
            return win32con.VK_RETURN
        elif key == Qt.Key_Enter:
            return win32con.VK_RETURN
        elif key == Qt.Key_Insert:
            return win32con.VK_INSERT
        elif key == Qt.Key_Delete:
            return win32con.VK_DELETE
        elif key == Qt.Key_Pause:
            return win32con.VK_PAUSE
        elif key == Qt.Key_Print:
            return win32con.VK_PRINT
        elif key == Qt.Key_Clear:
            return win32con.VK_CLEAR
        elif key == Qt.Key_Home:
            return win32con.VK_HOME
        elif key == Qt.Key_End:
            return win32con.VK_END
        elif key == Qt.Key_Left:
            return win32con.VK_LEFT
        elif key == Qt.Key_Up:
            return win32con.VK_UP
        elif key == Qt.Key_Right:
            return win32con.VK_RIGHT
        elif key == Qt.Key_Down:
            return win32con.VK_DOWN
        elif key == Qt.Key_PageUp:
            return win32con.VK_PRIOR
        elif key == Qt.Key_PageDown:
            return win32con.VK_NEXT
        elif key == Qt.Key_F1:
            return win32con.VK_F1
        elif key == Qt.Key_F2:
            return win32con.VK_F2
        elif key == Qt.Key_F3:
            return win32con.VK_F3
        elif key == Qt.Key_F4:
            return win32con.VK_F4
        elif key == Qt.Key_F5:
            return win32con.VK_F5
        elif key == Qt.Key_F6:
            return win32con.VK_F6
        elif key == Qt.Key_F7:
            return win32con.VK_F7
        elif key == Qt.Key_F8:
            return win32con.VK_F8
        elif key == Qt.Key_F9:
            return win32con.VK_F9
        elif key == Qt.Key_F10:
            return win32con.VK_F10
        elif key == Qt.Key_F11:
            return win32con.VK_F11
        elif key == Qt.Key_F12:
            return win32con.VK_F12
        elif key == Qt.Key_Space:
            return win32con.VK_SPACE
        elif key == Qt.Key_Asterisk:
            return win32con.VK_MULTIPLY
        elif key == Qt.Key_Plus:
            return win32con.VK_ADD
        elif key == Qt.Key_Comma:
            return win32con.VK_SEPARATOR
        elif key == Qt.Key_Minus:
            return win32con.VK_SUBTRACT
        elif key == Qt.Key_Slash:
            return win32con.VK_DIVIDE
        elif key == Qt.Key_MediaNext:
            return win32con.VK_MEDIA_NEXT_TRACK
        elif key == Qt.Key_MediaPrevious:
            return win32con.VK_MEDIA_PREV_TRACK
        elif key == Qt.Key_MediaPlay:
            return win32con.VK_MEDIA_PLAY_PAUSE
        elif key == Qt.Key_MediaStop:
            return win32con.VK_MEDIA_STOP
        elif key == Qt.Key_VolumeDown:
            return win32con.VK_VOLUME_DOWN
        elif key == Qt.Key_VolumeUp:
            return win32con.VK_VOLUME_UP
        elif key == Qt.Key_VolumeMute:
            return win32con.VK_VOLUME_MUTE
        elif key == Qt.Key_0:
            return key
        elif key == Qt.Key_1:
            return key
        elif key == Qt.Key_2:
            return key
        elif key == Qt.Key_3:
            return key
        elif key == Qt.Key_4:
            return key
        elif key == Qt.Key_5:
            return key
        elif key == Qt.Key_6:
            return key
        elif key == Qt.Key_7:
            return key
        elif key == Qt.Key_8:
            return key
        elif key == Qt.Key_9:
            return key
        elif key == Qt.Key_A:
            return key
        elif key == Qt.Key_B:
            return key
        elif key == Qt.Key_C:
            return key
        elif key == Qt.Key_D:
            return key
        elif key == Qt.Key_E:
            return key
        elif key == Qt.Key_F:
            return key
        elif key == Qt.Key_G:
            return key
        elif key == Qt.Key_H:
            return key
        elif key == Qt.Key_I:
            return key
        elif key == Qt.Key_J:
            return key
        elif key == Qt.Key_K:
            return key
        elif key == Qt.Key_L:
            return key
        elif key == Qt.Key_M:
            return key
        elif key == Qt.Key_N:
            return key
        elif key == Qt.Key_O:
            return key
        elif key == Qt.Key_P:
            return key
        elif key == Qt.Key_Q:
            return key
        elif key == Qt.Key_R:
            return key
        elif key == Qt.Key_S:
            return key
        elif key == Qt.Key_T:
            return key
        elif key == Qt.Key_U:
            return key
        elif key == Qt.Key_V:
            return key
        elif key == Qt.Key_W:
            return key
        elif key == Qt.Key_X:
            return key
        elif key == Qt.Key_Y:
            return key
        elif key == Qt.Key_Z:
            return key
        else:
            return 0

    def __registerHotkey(self, nativeKey, nativeMods):
        return User32.RegisterHotKey(0, nativeMods ^ nativeKey, nativeMods, nativeKey)

    def __unregisterHotkey(self, nativeKey, nativeMods):
        return User32.UnregisterHotKey(0, nativeMods ^ nativeKey)

    def __setHotkey(self):
        allMods = 0x02000000 | 0x04000000 | 0x08000000 | 0x10000000
        if self.hotkey.isEmpty():
            key = Qt.Key(0)
            mods = Qt.KeyboardModifier(0)
        else:
            key = Qt.Key((self.hotkey[0] ^ allMods) & self.hotkey[0])
            mods = Qt.KeyboardModifier(self.hotkey[0] & allMods)
        self.__nativeKey = self.__nativeKeycode(key)
        self.__nativeMods = self.__nativeModifiers(mods)
        res = self.__registerHotkey(self.__nativeKey, self.__nativeMods)
        if res:
            if not self.hotkeyCenter.addHotkey(self.__nativeKey, self.__nativeMods, self):
                self.exist = True
        return res

    def __unsetHokey(self):
        if self.exist:
            return True
        if self.hotkeyCenter.delHotkey(self.__nativeKey, self.__nativeMods):
            return self.__unregisterHotkey(self.__nativeKey, self.__nativeMods)
        else:
            return False
