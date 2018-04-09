#
#
#   Productivity App
#
#   by Christopher Medrano & Zachary Mitchell
#
#
#
#

import os


class AppFinder:
    def __init__(self):
        print("Getting Apps")
        self.shortcut_folder = 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs'
        self.shortcuts = []
        self.shortcut_names = []
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

    #This is where the shortcut will be executed
    def run_app(self, name):
        print("running app " + name)
        app_index = 0
        for i in range(len(self.shortcut_names)):
            if self.shortcut_names[i] == name:
                app_index = i
                break
        os.startfile(self.shortcuts[app_index])