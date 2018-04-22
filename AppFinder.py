#
#
#   Productivity App : AppFinder
#
#   by Christopher Medrano & Zachary Mitchell
#
#   Description: The app finder searches through the Start Menu's shortcuts
#                   in order to get a list of apps that can be opened
#                   from the productivity app. Run from the window manager.
#

import win32gui
import time
import os


class AppFinder:

    def __init__(self):
        print("@ af : init")
        self.shortcut_folder = 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs'
        self.window_search_timeout = 10
        self.shortcuts = []
        self.shortcut_names = []
        self.top_windows = []
        self.window_handle = []
        self.get_shortcuts()

    # collects shortcuts from Start Menu > Programs folder and creates
    # two arrays, one with full address for reference, and one with just
    # names for menu purposes
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

    # This is where the shortcut is executed using os.startfile
    # Called from Window manager when a name is double clicked
    # Waits for a handle to be received from the foreground
    # that isn't the original window's until window_search_timeout
    # is reached.
    def run_app(self, name):
        print("@ af : run_app : " + name)
        og_handle = win32gui.GetForegroundWindow()
        print("My app handle: " + str(og_handle))
        start_time = time.time()
        for i in range(len(self.shortcut_names)):
            if name == self.shortcut_names[i]:
                os.startfile(self.shortcuts[i])
                time.sleep(1)
                break

        handle = win32gui.GetForegroundWindow()
        while handle == og_handle:
            handle = win32gui.GetForegroundWindow()
            print("@ af : Checking " + str(handle))
            time.sleep(0.2)
            if time.time() - start_time >= self.window_search_timeout:
                print("@ af : Window Search timed out ;_;")
                return -1

        return handle
