#!/bin/sh

pyinstaller gui.py --noconfirm --onefile --windowed --add-data "C:/Users/DX/AppData/Local/Programs/Python/Python39/Lib/site-packages/customtkinter;customtkinter/" --hidden-import=plyer.platforms.win.notification --uac-admin --name POE自动药技能