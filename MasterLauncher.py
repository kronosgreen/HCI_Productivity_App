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
import _ctypes
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTabWidget, QTableWidget, QPushButton, QGridLayout, QMessageBox
from PyQt5.QtCore import QWaitCondition
import productivityApp as pa
import PopUpMenus as popup


class MasterLauncher(QMainWindow):
    def __init__(self):
        print("@ ml : init")
        super().__init__()
        self.start_time = time.time()

        self.tabs = QTabWidget()
        self.tab_count = 1
        self.tab_index = 0

        self.high_intensity_tasks = 7
        self.medium_intensity_tasks = 5
        self.light_intensity_tasks = 3
        self.s_tab_menu_open = False

        self.switch_tabs_action = QAction("&Switch Tabs", self)
        self.new_tab_action = QAction("&New Application", self)
        self.close_current_tab_action = QAction("&Close Current Tab", self)

        self.init_ui()

    def init_ui(self):
        first_tab = pa.AppWindow(self, 0)
        self.tabs.addTab(first_tab, "first_app")
        self.tabs.tabBar().setVisible(False)
        self.setCentralWidget(self.tabs)
        self.init_menu_bar()
        self.showFullScreen()

    # initialize the menu bar that shows up at the top
    def init_menu_bar(self):
        self.statusBar()

        main_menu = self.menuBar()
        options = main_menu.addMenu('&Options')

        settings_action = QAction("&Settings", self)
        settings_action.triggered.connect(self.open_settings)

        quit_action = QAction("&Quit Application", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close_app)

        self.new_tab_action.triggered.connect(self.create_new_tab)

        self.switch_tabs_action.triggered.connect(self.switch_tab)

        self.close_current_tab_action.triggered.connect(self.close_current_tab)

        options.addAction(settings_action)
        options.addAction(self.new_tab_action)
        options.addAction(self.switch_tabs_action)
        options.addAction(self.close_current_tab_action)
        options.addAction(quit_action)

        self.switch_tabs_action.setEnabled(False)
        self.close_current_tab_action.setEnabled(False)
        self.new_tab_action.setEnabled(False)

        help_menu = main_menu.addMenu('&Help')

        documentation_action = QAction("&Open Documentation", self)
        documentation_action.triggered.connect(self.open_documentation)

        help_menu.addAction(documentation_action)

    # close app and print time of use
    def close_app(self):
        print("@ close_app")
        print("Time of Productivity : " + str(time.time() - self.start_time))
        sys.exit()

    # open settings menu to set intensity task #'s and other such things
    def open_settings(self):
        print("@ ml : open_settings")

    # opens up new tab and goes to it
    def create_new_tab(self):
        print("@ ml : create_new_tab")
        self.tab_count += 1
        self.tab_index = self.tab_count - 1
        new_tab = pa.AppWindow(self, self.tab_index)
        self.tabs.addTab(new_tab, "new tab")
        self.tabs.setCurrentIndex(self.tab_index)
        self.switch_tabs_action.setEnabled(False)
        self.new_tab_action.setEnabled(False)
        self.close_current_tab_action.setEnabled(False)

    # close current tab, open a new one if none, otherwise allow user to switch to whatever tab
    def close_current_tab(self):
        print("@ ml : close_current_tab")
        self.tab_count -= 1
        self.tabs.removeTab(self.tab_index)
        if self.tab_count == 0:
            self.create_new_tab()
            self.tab_index = 0
        else:
            self.switch_tab()

    # direct user to the documentation online or something
    def open_documentation(self):
        print("@ ml : open_documentation")

    # opens the menu with available tabs to be able to switch to any one
    def switch_tab(self):
        print("@ ml : switch_tab")
        if not self.s_tab_menu_open:
            self.s_tab_menu_open = True
            tabs = []
            for tab in range(self.tab_count):
                tabs.append(self.tabs.tabText(tab))
            tab_menu = popup.TabTable(self)
            tab_menu.add_tabs(tabs)
            tab_menu.show()
            self.switch_tabs_action.setEnabled(False)
            self.new_tab_action.setEnabled(False)
            self.close_current_tab_action.setEnabled(False)

    # switches tab to specified tab
    def go_to_tab(self, index):
        print("@ ml : go_to_tab " + str(index))
        self.tab_index = index
        self.tabs.setCurrentIndex(self.tab_index)

    # sets the specified tab's text to the name of the application
    def change_tab_name(self, tab_index, tab_name):
        print("@ ml : change_tab_name")
        self.tabs.setTabText(tab_index, tab_name)

    # returns an array of the corresponding number of tasks to complete to intensity
    def get_intensities(self):
        print("@ ml : get_intensities")
        return [self.light_intensity_tasks, self.medium_intensity_tasks, self.high_intensity_tasks]

    # opens menu to select intensity before continuing
    def open_intensity_menu(self):
        print("@ ml : open_intensity_menu")
        intensity_menu = popup.IntensityMenu(self)
        intensity_menu.show()
        # intensity_menu.raise_()

    # opens menu that appears when all tasks are complete
    def complete(self):
        print("@ ml : complete")
        completion_menu = popup.TaskCompletionMenu(self)
        completion_menu.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MasterLauncher()
    sys.exit(app.exec_())
