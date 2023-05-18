import threading
import sys
import json
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
            data = [
                {"type": "自动技能", "key": "", "value": ""},
                {"type": "自动技能", "key": "", "value": ""},
                {"type": "自动技能", "key": "", "value": ""}
            ]
            json_str = json.dumps(data)
            f.write(json_str)
            return data
        
def save_config(data):
    with open('config.json', 'w', encoding="utf-8") as f:
        json_str = json.dumps(data)
        f.write(json_str)