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

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTabWidget, QWidget, QPushButton, QGridLayout

import productivityApp as pa


class MasterLauncher(QMainWindow):
    def __init__(self):
        print("@ ml : init")
        super().__init__()
        self.tabs = QTabWidget()
        self.tab_count = 1
        self.tab_index = 0

        self.high_intensity_tasks = 7
        self.medium_intensity_tasks = 5
        self.light_intensity_tasks = 3

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

        switch_tabs_action = QAction("&Switch Tabs", self)
        switch_tabs_action.triggered.connect(self.switch_tab)

        options.addAction(new_tab_action)
        options.addAction(switch_tabs_action)
        options.addAction(settings_action)
        options.addAction(quit_action)

        help_menu = main_menu.addMenu('&Help')

        documentation_action = QAction("&Open Documentation", self)
        documentation_action.triggered.connect(self.open_documentation)

        help_menu.addAction(documentation_action)

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
        tabs = []
        for tab in range(self.tab_count):
            tabs.append(self.tabs.tabText(tab))
        tab_menu = TabTable(self)
        tab_menu.add_tabs(tabs)

    def go_to_tab(self, index):
        print("@ ml : go_to_tab")
        self.tab_index = index
        self.tabs.setCurrentIndex(self.tab_index)

    def change_tab_name(self, tab_index, tab_name):
        print("@ ml : change_tab_name")
        self.tabs.setTabText(tab_index, tab_name)


class TabTable(QWidget):

    def __init__(self, parent=None):
        print("@ tab menu : init")
        super().__init__(parent)
        self.parent = parent
        self.show()

    def add_tabs(self, tabs):
        print("@ tab menu : add_tabs")
        layout = QGridLayout()
        self.setMinimumSize(400, 400)
        for tab in range(len(tabs)):
            tab_button = QPushButton(self)
            tab_button.setText(tabs[tab])
            tab_button.clicked.connect(lambda: self.switch_to_tab(tab))
            layout.addWidget(tab_button, tab, 0)
        self.setLayout(layout)

    def switch_to_tab(self, index):
        print("@ tab menu : go_to_tab : " + str(index))
        self.parent.go_to_tab(index)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MasterLauncher()
    sys.exit(app.exec_())
