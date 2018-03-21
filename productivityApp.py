#
#
#   Productivity App
#
#   by Christopher Medrano & Zachary Mitchell
#

import os
import ctypes
import win32api
import win32gui
import win32process
import re
from collections import namedtuple
from ctypes import byref, create_unicode_buffer, windll
from ctypes.wintypes import DWORD
from itertools import count
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QGridLayout, QLineEdit, QMainWindow, QScrollArea, QTextEdit, QListWidget, QDockWidget
from PyQt5.QtGui import QIcon, QWindow, QPageLayout, QActionEvent
from PyQt5.QtCore import Qt, pyqtSlot
import numpy as np

class ProductivityApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = 'Productivity App Prototype'
        self.top = 10
        self.left = 10
        self.height = 500
        self.width = 800
        self.windowManager = WindowManager(self)
        #self.testingApp = QWidget.createWindowContainer(QWindow.fromWinId(16144))
        #self.testingApp.setParent(self)
        self.taskMenu = TaskMenu(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar()
        mainMenu = self.menuBar()
        mainMenu.addMenu('&Options')
        mainMenu.addMenu('&Help')
        self.setCentralWidget(self.windowManager)
        self.addDockWidget(Qt.RightDockWidgetArea, self.taskMenu)
        self.show()

class WindowManager(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.title = 'Window Manager Prototype'
        self.top = 10
        self.left = 10
        self.height = 500
        self.width = 800
        self.winFinder = WindowFinder()
        self.appFinder = AppFinder()
        self.apps = self.appFinder.get_installed_products()
        self.appSearchBox = QLineEdit(self)
        self.availableApps = QListWidget(self)
        self.winManagerLayout = QGridLayout()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # os.startfile("C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD.EXE")
        # scrollArea = QScrollArea()
        # self.availableApps.setParent(scrollArea)
        # self.availableApps.setReadOnly(True)
        self.winManagerLayout.addWidget(self.appSearchBox, 0, 0)
        self.winManagerLayout.addWidget(self.availableApps, 1, 0)
        self.appSearchBox.textChanged.connect(self.updateAppList)
        self.setLayout(self.winManagerLayout)
        print("Install Location: " + self.apps[10].InstallLocation)
        print("check " + os.path.dirname(self.apps[2].InstalledProductName))
        self.show()

    def updateAppList(self):
        appName = self.appSearchBox.text()
        self.availableApps.clear()
        availableApps = ["none" for i in range(len(self.apps))]
        if len(appName) == 0:
            for i in range(len(availableApps)):
                availableApps[i] = self.apps[i].InstalledProductName
        else:
            #availableApps = np.empty(len(self.apps), dtype='s128')
            #array_iter = 0
            availableApps = []
            for j in range(100):
                matches = True
                for i in range(len(appName)):
                    if self.apps[j].InstalledProductName.upper()[i] != appName.upper()[i]:
                        matches = False
                        break
                if matches:
                    availableApps.append(self.apps[j].InstalledProductName)
                    #array_iter += 1
        self.availableApps.addItems(availableApps)



    def runApp(self):
        #do something here
        print("Run App: ")

    def addWindow(self, windowId):

        self.appWindow = QWindow.fromWinId(windowId)
        self.appWindow.setFlag(Qt.FramelessWindowHint, True)
        self.appWidget = QWidget.createWindowContainer(self.appWindow)


class TaskMenu(QDockWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = 'Task Menu Prototype'
        self.top = 10
        self.left = 10
        self.height = 500
        self.width = 800
        self.totalTasksCompleted = 0
        self.tasksCompleted = 0
        self.taskList = []
        self.taskIndex = 2
        self.textBox = QLineEdit(self)
        self.taskLayout = QGridLayout()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color:cyan")
        buttonLayout = QGridLayout()
        self.addTaskButton = QPushButton(self)
        self.addTaskButton.setText("Add Task")
        buttonLayout.addWidget(self.addTaskButton, 0, 0)
        self.removeTaskButton = QPushButton(self)
        self.removeTaskButton.setText("Remove Task")
        buttonLayout.addWidget(self.removeTaskButton, 0,1)
        self.clearTasksButton = QPushButton(self)
        self.clearTasksButton.setText("Clear Tasks")
        buttonLayout.addWidget(self.clearTasksButton, 0, 2)
        self.taskLayout.addLayout(buttonLayout, 0, 0)
        self.taskLayout.addWidget(self.textBox, 1, 0)
        self.setLayout(self.taskLayout)
        self.show()

    @pyqtSlot()
    def addTask(self):
        text = self.textBox.text()
        newButton = QPushButton(self)
        newButton.setText(text)
        self.taskLayout.addWidget(newButton, self.taskIndex, 0)
        self.taskIndex += 1
        print("add")

    def completeTask(self):
        print("completed")

    def clearTasks(self):
        print("clear")

class WindowFinder:

    """Class to find and make focus on a particular Native OS dialog/Window """
    def __init__(self):
        self._handle = None

    def find_window(self, window_name):
        """Pass a window class name & window name directly if known to get the window """
        self._handle = win32gui.FindWindow(None, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        '''Call back func which checks each open window and matches the name of window using reg ex'''
        window_name = str(win32gui.GetWindowText(hwnd))
        if re.match(wildcard, window_name) != None:
            pid = win32process.GetWindowThreadProcessId(hwnd)
            print("Found matching window: %s  - With PID: %s" % (window_name, pid))
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """ This function takes a string as input and calls EnumWindows to enumerate through all open windows """
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """Get the focus on the desired open window"""
        win32gui.SetForegroundWindow(self._handle)

    def get_window_handler(self):
        return self._handle


class AppFinder:
    # defined at http://msdn.microsoft.com/en-us/library/aa370101(v=VS.85).aspx
    def __init__(self):
        self.UID_BUFFER_SIZE = 39
        self.PROPERTY_BUFFER_SIZE = 256
        self.ERROR_MORE_DATA = 234
        self.ERROR_INVALID_PARAMETER = 87
        self.ERROR_SUCCESS = 0
        self.ERROR_NO_MORE_ITEMS = 259
        self.ERROR_UNKNOWN_PRODUCT = 1605
        # diff propoerties of a product, not all products have all properties
        self.PRODUCT_PROPERTIES = [u'Language',
                          u'ProductName',
                          u'PackageCode',
                          u'Transforms',
                          u'AssignmentType',
                          u'PackageName',
                          u'InstalledProductName',
                          u'VersionString',
                          u'RegCompany',
                          u'RegOwner',
                          u'ProductID',
                          u'ProductIcon',
                          u'InstallLocation',
                          u'InstallSource',
                          u'InstallDate',
                          u'Publisher',
                          u'LocalPackage',
                          u'HelpLink',
                          u'HelpTelephone',
                          u'URLInfoAbout',
                          u'URLUpdateInfo', ]

        # class to be used for python users :)
        self.Product = namedtuple('Product', self.PRODUCT_PROPERTIES)


    def get_property_for_product(self, product, property, buf_size=256):
        """Retruns the value of a fiven property from a product."""
        property_buffer = create_unicode_buffer(buf_size)
        size = DWORD(buf_size)
        result = windll.msi.MsiGetProductInfoW(product, property, property_buffer,
                                               byref(size))
        if result == self.ERROR_MORE_DATA:
            return self.get_property_for_product(product, property,
                                            2 * buf_size)
        elif result == self.ERROR_SUCCESS:
            return property_buffer.value
        else:
            return None


    def populate_product(self, uid):
        """Return a Product with the different present data."""
        properties = []
        for property in self.PRODUCT_PROPERTIES:
            properties.append(self.get_property_for_product(uid, property))
        return self.Product(*properties)


    def get_installed_products_uids(self):
        """Returns a list with all the different uid of the installed apps."""
        # enum will return an error code according to the result of the app
        products = []
        for i in count(0):
            uid_buffer = create_unicode_buffer(self.UID_BUFFER_SIZE)
            result = windll.msi.MsiEnumProductsW(i, uid_buffer)
            if result == self.ERROR_NO_MORE_ITEMS:
                # done interating over the collection
                break
            products.append(uid_buffer.value)
        return products


    def get_installed_products(self):
        """Returns a collection of products that are installed in the system."""
        products = []
        for puid in self.get_installed_products_uids():
            products.append(self.populate_product(puid))
        return products


    def is_product_installed_uid(self, uid):
        """Return if a product with the given id is installed.

        uid Most be a unicode object with the uid of the product using
        the following format {uid}
        """
        # we try to get the VersisonString for the uid, if we get an error it means
        # that the product is not installed in the system.
        buf_size = 256
        uid_buffer = create_unicode_buffer(uid)
        property = u'VersionString'
        property_buffer = create_unicode_buffer(buf_size)
        size = DWORD(buf_size)
        result = windll.msi.MsiGetProductInfoW(uid_buffer, property, property_buffer,
                                               byref(size))
        if result == self.ERROR_UNKNOWN_PRODUCT:
            return False
        else:
            return True



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProductivityApp()
    sys.exit(app.exec_())
