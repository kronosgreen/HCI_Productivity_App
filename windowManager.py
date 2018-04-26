#
#
#   Productivity App
#
#   by Christopher Medrano & Zachary Mitchell
#
#
#
#

from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QListWidget
from PyQt5.QtGui import QWindow
from PyQt5.QtCore import Qt

import AppFinder as ap


class WindowManager(QWidget):

    def __init__(self, parent):
        print("@ wm : init")
        super().__init__(parent)
        self.parent = parent
        self.title = 'Window Manager Prototype'
        self.widgets_active = True
        self.app_widget = None
        self.app_window = None
        self.appFinder = ap.AppFinder(self)
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
        if whnd == -1:
            print("wm : Error, could not get window handle")
            return
        self.set_to_window(whnd)
        self.parent.change_tab_name(app_name)

    def set_to_window(self, window_id):
        print("@ wm : set_to_window : " + str(window_id))
        if self.widgets_active:
            self.winManagerLayout.removeWidget(self.appSearchBox)
            self.appSearchBox.deleteLater()
            self.winManagerLayout.removeWidget(self.availableApps)
            self.availableApps.deleteLater()
            self.widgets_active = False
        try:
            self.app_window = QWindow.fromWinId(window_id)
        except RuntimeError:
            print("Sorry, Run Time Error ;_;")
        except OSError:
            print("Sorry, OS Error ;_;")
        else:
            self.app_window.setFlag(Qt.FramelessWindowHint, True)
            self.app_widget = QWidget.createWindowContainer(self.app_window, self, Qt.FramelessWindowHint)
            self.winManagerLayout.addWidget(self.app_widget, 0, 0)
            self.app_widget.show()
