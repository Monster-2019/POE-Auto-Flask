import customtkinter
import tkinter as tk
import keyboard
import os
from script import AutoPotionSkill
from utils import load_config, save_config


class MyPotionSkillFrams(customtkinter.CTkFrame):
    def __init__(self, master, config, row):
        super().__init__(master)

        self.row = row
        self.type = config["type"]

        self.configure(fg_color="#ebebeb")
        self.grid_columnconfigure((0,1,2), weight=1)

        self.optionmenu = customtkinter.CTkOptionMenu(self, values=["自动技能", "百分比吃药"],
                                         command=self.optionmenu_callback)
        self.optionmenu.set(self.type)
        self.optionmenu.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.key = config["key"]
        self.value = config["value"]

        self.init_entry()

    def init_entry(self):
        if self.type == '自动技能':
            placeholder_key = "技能按键"
            placeholder_value = "冷却时间(秒)"
        if self.type == '百分比吃药':
            placeholder_key = "药剂键位"
            placeholder_value = "百分比"
        if self.key:
            self.entry1 = customtkinter.CTkEntry(self, placeholder_text=placeholder_key, textvariable=tk.StringVar(value=self.key))
        else:
            self.entry1 = customtkinter.CTkEntry(self, placeholder_text=placeholder_key)
        self.entry1.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        if self.value:
            self.entry2 = customtkinter.CTkEntry(self, placeholder_text=placeholder_value, textvariable=tk.StringVar(value=self.value))
        else:
            self.entry2 = customtkinter.CTkEntry(self, placeholder_text=placeholder_value)
        self.entry2.grid(row=0, column=2, padx=10, pady=10, sticky="ew")


    def optionmenu_callback(self, val):
        self.type = val
        self.init_entry()

    def get_value(self):
        return {"type": self.type, "key": self.entry1.get(), "value": self.entry2.get()}


class MyButtonFrams(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.starting = False
        self.autoPotionSkill = AutoPotionSkill()

        self.configure(fg_color="#ebebeb")
        self.grid_columnconfigure((0,1), weight=1)

        self.savebtn = customtkinter.CTkButton(self, text="保存", command=self.save)
        self.savebtn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.startbtn = customtkinter.CTkButton(self, text="F2 启动/终止", command=self.start)
        self.startbtn.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.startbtn.bind("<F2>", lambda event: self.button.invoke())

    def save(self):
        self.master.save()
        self.autoPotionSkill = AutoPotionSkill()

    def start(self):
        self.autoPotionSkill.run()
    

class PotionSkillGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.configData = load_config()
        self.config = []

        self.title("POE 自动药技能")
        self.geometry("500x200")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        for i in range(3):
            MyPotionSkill = MyPotionSkillFrams(self, self.configData[i], i)
            MyPotionSkill.grid(row=i, column=0, padx=0, pady=0, sticky="ew")
            self.config.append(MyPotionSkill)

        self.MyButtonFrams = MyButtonFrams(self)
        self.MyButtonFrams.grid(row=3, column=0, padx=0, pady=0, sticky="sew")

        keyboard.add_hotkey('F2', self.MyButtonFrams.start)

    def save(self):
        data = []
        for c in self.config:
            c_data = c.get_value()
            data.append(c_data)
        save_config(data)

# app = App()
# app.mainloop()

if __name__ == "__main__":
    try:
        app = PotionSkillGUI()
        app.mainloop()
    except Exception:
        os._exit(0)