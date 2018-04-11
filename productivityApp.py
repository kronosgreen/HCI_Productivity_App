#
#
#   Productivity App
#
#   by Christopher Medrano & Zachary Mitchell
#
#
#
#

import sys

from PyQt5.QtWidgets import QWidget, QGridLayout

import taskMenu as tm
import windowManager as wm


class AppWindow(QWidget):
    
    def __init__(self, parent, tab_index):
        print("@ aw : init")
        super().__init__()
        self.parent = parent
        self.title = 'Productivity App Window'
        self.tab_index = tab_index
        self.intensity = 3
        self.windowManager = wm.WindowManager(self)
        self.taskMenu = tm.TaskMenu(self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        layout = QGridLayout()

        layout.addWidget(self.windowManager, 0, 0)
        self.taskMenu.setMaximumWidth(500)
        layout.addWidget(self.taskMenu, 0, 1)

        self.setLayout(layout)

    def set_intensity(self, intensity):
        print("@ aw : set_intensity")
        self.intensity = intensity
        if intensity == 1:
            self.taskMenu.set_tasks_till_completion(3)
        elif intensity == 2:
            self.taskMenu.set_tasks_till_completion(5)
        elif intensity == 3:
            self.taskMenu.set_tasks_till_completion(7)

    # called when an app is opened
    def change_tab_name(self, tab_name):
        print("@ aw : change_tab_name & window opened")
        self.parent.change_tab_name(self.tab_index, tab_name)
        self.taskMenu.set_window_opened(True)
