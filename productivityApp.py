#
#
#   Productivity App
#
#   by Christopher Medrano & Zachary Mitchell
#
#
#
#

from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.Qt import QRegion

import taskMenu as tm
import windowManager as wm


class AppWindow(QWidget):
    
    def __init__(self, parent, tab_index):
        print("@ aw : init")
        super().__init__()
        self.parent = parent
        self.title = 'Productivity App Window'
        self.region = None
        self.tab_index = tab_index
        self.intensity = 3
        self.windowManager = wm.WindowManager(self)
        self.taskMenu = tm.TaskMenu(self)
        self.init_ui()

    def init_ui(self):
        print("@ aw : init_ui")
        self.setWindowTitle(self.title)
        layout = QGridLayout()

        layout.addWidget(self.windowManager, 0, 0)
        self.taskMenu.setMaximumWidth(500)
        layout.addWidget(self.taskMenu, 0, 1)

        self.setLayout(layout)

    # Sets intensity by level
    def set_intensity(self, intensity):
        print("@ aw : set_intensity")
        self.intensity = intensity
        task_numbers = self.parent.get_intensities()
        self.taskMenu.set_tasks_till_completion(task_numbers[intensity - 1])

    # disable window manager if
    def set_enable_window(self, enable):
        print("@ aw : set_enable_window")
        '''
        if not enable:
            self.region = QRegion(self.windowManager.geometry())
            self.windowManager.setMask(self.region)
        else:
            print("Good luck")
            del self.region
         '''

    # Disable app to stop receiving input while the intensity is being collected
    # and open menu to set intensity of task
    def app_is_run(self):
        print("@ aw : app_is_run")
        self.set_enable_window(False)
        self.parent.open_intensity_menu()

    # App is opened, now update the task manager, update the main app
    # to include the app name, and start collecting information to start
    # session.
    def change_tab_name(self, tab_name):
        print("@ aw : change_tab_name & window opened")
        self.parent.change_tab_name(self.tab_index, tab_name)
        self.taskMenu.set_window_opened(True)
        self.app_is_run()
