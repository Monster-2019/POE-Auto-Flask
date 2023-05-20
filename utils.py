import threading
import sys
import json
import win32gui, win32api, win32con
import ctypes
from time import sleep

class PauseableThread(threading.Thread):
    def __init__(self, target, args=()):
        super(PauseableThread, self).__init__()
        self.target = target
        self.args = args
        self.pause = False    # 用于暂停线程的标识
        self.stop = False    # 用于停止线程的标识

    def run(self):
        sys.settrace(self.trace_func)
        if self.args:
            self.target(*self.args)
        else:
            self.target()

    def trace_func(self, frame, event, arg):
        if self.pause:
            while self.pause:
                sleep(0.1)
        if self.stop:
            sys.exit()
        return self.trace_func

    def pause_thread(self):
        self.pause = True

    def resume_thread(self):
        self.pause = False

    def stop_thread(self):
        self.stop = True

def load_config():
    try:
        with open('config.json', 'r', encoding="utf-8") as f:
            json_str = f.read()
            data = json.loads(json_str)
            return data
    except FileNotFoundError:
        with open('config.json', 'w', encoding="utf-8") as f:
            data = [{"type": "自动技能", "key": "", "value": ""} for _ in range(5)]
            json_str = json.dumps(data)
            f.write(json_str)
            return data
        
def save_config(data):
    with open('config.json', 'w', encoding="utf-8") as f:
        json_str = json.dumps(data)
        f.write(json_str)

WINDOW_HEIGHT = 1080
ONE_PERCENT = 210 / 100
LOW_BLOOD_RED = 92
WATCH_BLOOD_X = 110

class WatchClient():
    def __init__(self, widnow_name):
        super(WatchClient, self).__init__()
        self.hwnd = win32gui.FindWindow(None, widnow_name)
        self.gdi32 = ctypes.windll.gdi32
        self.hdc = ctypes.windll.user32.GetDC(self.hwnd)

    def get_color(self, x, y):
        # win32gui.SetForegroundWindow(self.hwnd)
        color = self.gdi32.GetPixel(self.hdc, x, y)
        r = color & 0xFF
        g = (color & 0xFF00) >> 8
        b = (color & 0xFF0000) >> 16
        
        return (r,g,b)
    
    def is_val_ready(self, x):
        r, g, b = self.get_color(x, 1025)
        print(r,g,b)
        if r > 129 and g > 129 and b > 129:
            return True
        
    def watch_HP(self, percent):
        percent_pa = int(WINDOW_HEIGHT - percent * ONE_PERCENT)
        red, green, blue = self.get_color(WATCH_BLOOD_X, percent_pa)
        print(red, green, blue)
        if red < LOW_BLOOD_RED:
            return True
        return False
    
    def press(self, key):
        ascii_key = ord(str(key))
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, ascii_key, 0)
        win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, ascii_key, 0)