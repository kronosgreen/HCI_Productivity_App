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

'''class WindowFinder:

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
    def __init__(self):
        print("Getting Apps")
        self.shortcut_folder = 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs'
        self.shortcuts = []
        self.shortcut_names = []
        self.get_shortcuts()

    def get_shortcuts(self):
        shortcuts = []
        shortcut_names = []
        for root, dirs, files in os.walk(self.shortcut_folder):
            for file in files:
                if file.endswith(".lnk"):
                    shortcut_names.append(os.path.splitext(file)[0])
                    shortcuts.append(os.path.join(root, file))
        self.shortcuts = shortcuts
        self.shortcut_names = shortcut_names

    #This is where the shortcut will be executed
    def run_app(self, name):
        print("running app " + name)
        app_index = 0
        for i in range(len(self.shortcut_names)):
            if self.shortcut_names[i] == name:
                app_index = i
                break
        os.startfile(self.shortcuts[app_index])'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProductivityApp()
    sys.exit(app.exec_())