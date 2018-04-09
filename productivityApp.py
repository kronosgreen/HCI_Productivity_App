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

from PyQt5.QtWidgets import QWidget, QApplication,QMainWindow, QDockWidget, QAction
from PyQt5.QtCore import Qt

import taskMenu as tm
import windowManager as wm

class ProductivityApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = 'Productivity App Prototype'
        self.windowManager = wm.WindowManager(self)
        self.taskDock = QDockWidget()
        self.taskMenu = tm.TaskMenu(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setCentralWidget(self.windowManager)
        self.addDockWidget(Qt.RightDockWidgetArea, self.taskDock)
        self.taskDock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.taskDock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.taskDock.setWidget(self.taskMenu)
        self.init_menu_bar()
        self.showFullScreen()

    def init_menu_bar(self):
        self.statusBar()

        main_menu = self.menuBar()
        options = main_menu.addMenu('&Options')
        help = main_menu.addMenu('&Help')

        settings_action = QAction("&Settings", self)
        settings_action.triggered.connect(self.open_settings)

        quit_action = QAction("&Quit Application", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close_app)

        options.addAction(quit_action)

    def close_app(self):
        print("Closing App")
        sys.exit()

    def open_settings(self):
        print("Opening Settings")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProductivityApp()
    sys.exit(app.exec_())