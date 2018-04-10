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
        self.parent = parent
        self.title = 'Window Manager Prototype'
        self.appFinder = ap.AppFinder()
        self.apps = self.appFinder.shortcut_names
        self.appSearchBox = QLineEdit(self)
        self.availableApps = QListWidget(self)
        self.availableApps.itemDoubleClicked.connect(self.run_app)
        self.update_app_list()
        self.winManagerLayout = QGridLayout()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.winManagerLayout.addWidget(self.appSearchBox, 0, 0)
        self.winManagerLayout.addWidget(self.availableApps, 1, 0)
        self.appSearchBox.textChanged.connect(self.update_app_list)
        self.setLayout(self.winManagerLayout)
        self.show()

    # search function
    def update_app_list(self):
        app_name = self.appSearchBox.text()
        self.availableApps.clear()
        if len(app_name) == 0:
            available_apps = self.apps
        else:
            available_apps = []
            for j in range(len(self.apps)):
                matches = True
                for i in range(len(app_name)):
                    if self.apps[j].upper()[i] != app_name.upper()[i]:
                        matches = False
                        break
                if matches:
                    available_apps.append(self.apps[j])
        self.availableApps.addItems(available_apps)

    # sends name of the button clicked to the app finder class which runs the app
    def run_app(self):
        print("@ wm : run_app")
        app_name = self.availableApps.currentItem().text()
        whnd = self.appFinder.run_app(app_name)
        self.parent.change_tab_name(app_name)
        # self.set_to_window(whnd)

    def set_to_window(self, window_id):
        print("@ wm : Setting to this Window")
        app_window = QWindow.fromWinId(window_id)
        self.app_window.setFlag(Qt.FramelessWindowHint, True)
        app_widget = QWidget.createWindowContainer(app_window)
