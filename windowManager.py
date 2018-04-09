#
#
#   Productivity App
#
#   by Christopher Medrano & Zachary Mitchell
#
#
#
#


from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QGridLayout, QLineEdit, \
    QMainWindow, QListWidget, QDockWidget, \
    QLayout, QAction
from PyQt5.QtGui import QIcon, QWindow, QPageLayout, QActionEvent
from PyQt5.QtCore import Qt, pyqtSlot, QObject

import AppFinder as ap


class WindowManager(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.title = 'Window Manager Prototype'
        self.top = 10
        self.left = 10
        self.height = 500
        self.width = 800
        self.appFinder = ap.AppFinder()
        self.apps = self.appFinder.shortcut_names
        self.appSearchBox = QLineEdit(self)
        self.availableApps = QListWidget(self)
        self.availableApps.itemDoubleClicked.connect(self.run_app)
        self.updateAppList()
        self.winManagerLayout = QGridLayout()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.winManagerLayout.addWidget(self.appSearchBox, 0, 0)
        self.winManagerLayout.addWidget(self.availableApps, 1, 0)
        self.appSearchBox.textChanged.connect(self.updateAppList)
        self.setLayout(self.winManagerLayout)
        self.show()

    def updateAppList(self):
        app_name = self.appSearchBox.text()
        self.availableApps.clear()
        if len(app_name) == 0:
            availableApps = self.apps
        else:
            #availableApps = np.empty(len(self.apps), dtype='s128')
            #array_iter = 0
            availableApps = []
            for j in range(len(self.apps)):
                matches = True
                for i in range(len(app_name)):
                    if self.apps[j].upper()[i] != app_name.upper()[i]:
                        matches = False
                        break
                if matches:
                    availableApps.append(self.apps[j])
                    #array_iter += 1'''
        self.availableApps.addItems(availableApps)

    def run_app(self):
        self.appFinder.run_app(self.availableApps.currentItem().text())
        #self.set_to_window()

    def set_to_window(self):
        print("Setting to this Window")

    def add_window(self, windowId):

        self.appWindow = QWindow.fromWinId(windowId)
        self.appWindow.setFlag(Qt.FramelessWindowHint, True)
        self.appWidget = QWidget.createWindowContainer(self.appWindow)