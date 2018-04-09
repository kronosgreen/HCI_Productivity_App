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
        self.top = 10
        self.left = 10
        self.height = 500
        self.width = 800
        self.windowManager = wm.WindowManager(self)
        #self.testingApp = QWidget.createWindowContainer(QWindow.fromWinId(16144))
        #self.testingApp.setParent(self)
        self.taskDock = QDockWidget()
        self.taskMenu = tm.TaskMenu(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
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
        main_menu.addMenu('&Options')
        main_menu.addMenu('&Help')

        quit_action = QAction("&Quit Application", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close_app)

        main_menu.addAction(quit_action)

    def close_app(self):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProductivityApp()
    sys.exit(app.exec_())