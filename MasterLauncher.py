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

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTabWidget

import productivityApp as pa


class MasterLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()
        self.tab_count = 1
        self.tab_index = 0
        self.init_ui()

    def init_ui(self):
        first_tab = pa.AppWindow(self, 0)
        self.tabs.addTab(first_tab, "first_app")
        # self.tabs.tabBar().setVisible(False)
        self.setCentralWidget(self.tabs)
        self.init_menu_bar()
        self.showFullScreen()

    def init_menu_bar(self):
        self.statusBar()

        main_menu = self.menuBar()
        options = main_menu.addMenu('&Options')

        settings_action = QAction("&Settings", self)
        settings_action.triggered.connect(self.open_settings)

        quit_action = QAction("&Quit Application", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close_app)

        new_tab_action = QAction("&New Application", self)
        new_tab_action.triggered.connect(self.create_new_tab)

        options.addAction(new_tab_action)
        options.addAction(settings_action)
        options.addAction(quit_action)

        help = main_menu.addMenu('&Help')

        documentation_action = QAction("&Open Documentation", self)
        documentation_action.triggered.connect(self.open_documentation)

    def close_app(self):
        print("@ close_app")
        sys.exit()

    def open_settings(self):
        print("@ ml : open_settings")

    def create_new_tab(self):
        print("@ ml : create_new_tab")
        self.tab_count += 1
        self.tab_index = self.tab_count - 1
        new_tab = pa.AppWindow(self, self.tab_index)
        self.tabs.addTab(new_tab, "new tab")
        self.tabs.setCurrentIndex(self.tab_index)

    def close_current_tab(self):
        print("@ ml : close_current_tab")
        self.tab_count -= 1
        # set new tab index and such

    def open_documentation(self):
        print("@ ml : open_documentation")

    def switch_tab(self):
        print("@ ml : switch_tab")

    def change_tab_name(self, tab_index, tab_name):
        print("@ ml : change_tab_name")
        self.tabs.setTabText(tab_index, tab_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MasterLauncher()
    sys.exit(app.exec_())
