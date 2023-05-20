from time import sleep
from utils import load_config, PauseableThread, WatchClient
from plyer import notification

threads = []
SKILL_Y = {
    "Q": 1422,
    "W": 1478,
    "E": 1534,
    "R": 1590,
    "T": 1646,
}

class AutoPotionSkill():
    def __init__(self):
        super().__init__()
        self.client = WatchClient('Path of Exile')

        config = load_config()
        self.config = [obj for obj in config if all(obj.values())]

        self.watching = False

    def auto_skill(self, key, time):
        while True:
            self.client.press(key)
            sleep(int(float(time)))

    def auto_eat_potion(self, key, percentage):
        while True:
            if self.client.watch_HP(int(percentage)):
                self.client.press(key)
            sleep(0.2)

    def auto_val_skill(self, key):
        while True:
            if self.client.is_val_ready(SKILL_Y[key]):
                self.client.press(key)
            sleep(0.2)
    
    
    def start(self):
        print('开始脚本')
        global threads
        for c in self.config:
            if c['type'] == '自动技能':
                t = PauseableThread(target=self.auto_skill,
                                    args=(c['key'], c['value']))
            if c['type'] == '百分比吃药':
                t = PauseableThread(target=self.auto_eat_potion,
                                    args=(c['key'], c['value']))
            if c['type'] == '自动瓦尔技能':
                t = PauseableThread(target=self.auto_val_skill,
                                    args=(c['key']))
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