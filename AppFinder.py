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
        print("@ af : init")
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

    # This is where the shortcut will be executed
    # called from window manager after double click
    def run_app(self, name):
        print("@ af : run_app : " + name)
        for i in range(len(self.shortcut_names)):
            if name == self.shortcut_names[i]:
                os.startfile(self.shortcuts[i])
                break
        handle = self.get_window_handle()
        return handle

    def get_window_handle(self):
        # find application just opened
        # get handle number from said application and return
        hnd = 1111
        return hnd