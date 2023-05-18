import win32gui, win32api, win32con
import ctypes
from time import sleep
from utils import load_config, PauseableThread
from plyer import notification

threads = []

class AutoPotionSkill():
    def __init__(self):
        super().__init__()

        self.hwnd = win32gui.FindWindow(None, "Path of Exile")
        config = load_config()
        self.config = [obj for obj in config if all(obj.values())]

        self.gdi32 = ctypes.windll.gdi32
        self.hdc = ctypes.windll.user32.GetDC(self.hwnd)
        self.one_percent = 210 / 100
        self.min_red = 92
        self.widnow_height = 1080
        self.watch_x = 110

        self.watching = False
    
    def press(self, key):
        ascii_key = ord(str(key))
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, ascii_key, 0)
        win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, ascii_key, 0)

    def auto_skill(self, key, time):
        while True:
            self.press(key)
            sleep(int(float(time)))

    def auto_eat_potion(self, key, percentage):
        while True:
            if self.watch_HP(int(percentage)):
                self.press(key)
            sleep(0.2)

    def watch_HP(self, percent):
        percent_pa = int(self.widnow_height - percent * self.one_percent)
        color = color = self.gdi32.GetPixel(self.hdc, self.watch_x, percent_pa)
        red = color & 0xFF
        if red < self.min_red:
            return True
        return False
    
    def start(self):
        print('开始脚本')
        global threads
        for c in self.config:
            if c['type'] == '自动技能':
                t = PauseableThread(target=self.auto_skill,
                                    args=(c['key'], c['value']))
                t.start()
                threads.append(t)
            if c['type'] == '百分比吃药':
                t = PauseableThread(target=self.auto_eat_potion,
                                    args=(c['key'], c['value']))
                t.start()
                threads.append(t)
                
    def stop(self):
        global threads
        for thread in threads:
            thread.stop_thread()
        print('结束脚本')

    def run(self):
        if not self.watching:
            self.start()
            self.watching = True
            notification.notify("POE 自动技能药通知", "辅助已开启", timeout=1)
        else:
            self.stop()
            self.watching = False
            notification.notify("POE 自动技能药通知", "辅助已关闭", timeout=1)