#
#
#   Productivity App
#
#   by Christopher Medrano & Zachary Mitchell
#
#
#
#
import win32gui
import time
import os


class AppFinder:
    def __init__(self):
        print("@ af : init")
        self.shortcut_folder = 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs'
        self.shortcuts = []
        self.shortcut_names = []
        self.top_windows = []
        self.window_handle = []
        self.get_shortcuts()

    def get_shortcuts(self):
        shortcuts = []
        shortcut_names = []
        for root, dirs, files in os.walk(self.shortcut_folder):
            for file in files:
                if file.endswith(".lnk"):
                    shortcut_names.append(os.path.splitext(file)[0])
                    shortcuts.append(os.path.join(root, file))
        self.shortcuts = shortcuts
        self.shortcut_names = shortcut_names

    # This is where the shortcut will be executed
    # called from window manager after double click
    def run_app(self, name):

        print("@ af : run_app : " + name)
        for i in range(len(self.shortcut_names)):
            if name == self.shortcut_names[i]:
                os.startfile(self.shortcuts[i])
                time.sleep(1)
                break
        handle = win32gui.GetForegroundWindow()
        return handle