#
#
#   Productivity App : Pop-up Menus
#
#   by Christopher Medrano & Zachary Mitchell
#
#
#
#

from PyQt5.QtWidgets import QApplication, QTableWidget, QPushButton, QGridLayout, QStyle, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


# QTableWidget that holds available tabs and allows user to switch
class TabTable(QTableWidget):

    def __init__(self, parent=None):
        print("@ tab menu : init")
        super().__init__(parent)
        self.parent = parent
        # self.setMinimumSize(600, 600)
        # self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.setMinimumSize(self.parent.tabs.widget(0).taskMenu.width(),
                            QApplication.desktop().screen().rect().height())
        # Aligns to right
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(),
                                            QApplication.desktop().availableGeometry()))

    def add_tabs(self, tabs):
        print("@ tab menu : add_tabs")
        layout = QGridLayout()
        for tab in range(len(tabs)):
            tab_button = QPushButton(self)
            tab_button.setText(tabs[tab])
            tab_button.clicked.connect(self.create_switch_function(tab))
            layout.addWidget(tab_button, tab, 0)
        self.setLayout(layout)

    def create_switch_function(self, x):
        return lambda y: self.switch_to_tab(x)

    def switch_to_tab(self, index):
        print("@ tab menu : go_to_tab : " + str(index))
        self.parent.go_to_tab(index)
        self.parent.s_tab_menu_open = False
        self.close()


# Allows user to set intensity of app opened
class IntensityMenu(QTableWidget):

    def __init__(self, parent=None):
        print("@ Intensity Menu : init")
        super().__init__(parent)
        self.setWindowTitle("Set Task Intensity")
        self.parent = parent
        self.setMinimumSize(self.parent.tabs.widget(0).taskMenu.width(), QApplication.desktop().screen().rect().height())
        # Aligns to right
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(),
                                            QApplication.desktop().availableGeometry()))
        self.add_intensity_buttons()

    def add_intensity_buttons(self):
        print("@ Intensity Menu : add_intensity_buttons")
        layout = QGridLayout()
        label = QLabel()
        label.setText("Set intensity of the task, please:")
        label.setMaximumHeight(50)
        layout.addWidget(label, 0, 0)
        intensity_nums = self.parent.get_intensities()
        intensities = ["Light Intensity " + str(intensity_nums[0]),
                       "Medium Intensity " + str(intensity_nums[1]),
                       "High Intensity " + str(intensity_nums[2])]
        for i in range(len(intensities)):
            intensity_button = QPushButton(self)
            intensity_button.setText(intensities[i])
            intensity_button.clicked.connect(self.create_intensity_function(i + 1))
            layout.addWidget(intensity_button, i + 1, 0)
        self.setLayout(layout)

    def create_intensity_function(self, x):
        return lambda y: self.set_intensity(x)

    def set_intensity(self, x):
        self.parent.tabs.widget(self.parent.tabs.currentIndex()).set_intensity(x)
        self.close()


# Menu that appears when tasks are completed
class TaskCompletionMenu(QTableWidget):

    def __init__(self, parent=None):
        print("@ Task Completion Menu : init")
        super().__init__(parent)
        self.setWindowTitle("Set Task Intensity")
        self.parent = parent
        self.setMinimumSize(self.parent.tabs.widget(0).taskMenu.width(), QApplication.desktop().screen().rect().height())
        # Aligns to right
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(),
                                            QApplication.desktop().availableGeometry()))
        self.init_ui()

    def init_ui(self):
        print("@ Task Completion Menu : init_ui")
        layout = QGridLayout()
        label = QLabel()
        label.setText("Congratulations!\nYou've completed your desired amount of tasks!\n\n"
                      "Please decide what you'd like to do now")
        layout.addWidget(label, 0, 0)

        continue_button = QPushButton(self)
        continue_button.setText("Continue")
        continue_button.clicked.connect(self.continue_task)
        layout.addWidget(continue_button, 1, 0)

        switch_task_button = QPushButton(self)
        switch_task_button.setText("Switch Tasks")
        switch_task_button.clicked.connect(self.switch_tasks)
        layout.addWidget(switch_task_button, 2, 0)

        new_task_button = QPushButton(self)
        new_task_button.setText("Start New Task")
        new_task_button.clicked.connect(self.new_task)
        layout.addWidget(new_task_button, 3, 0)

        quit_button = QPushButton(self)
        quit_button.setText("Quit, I'm all done! \(^-^)/")
        quit_button.clicked.connect(self.quit)
        layout.addWidget(quit_button, 4, 0)

        congrats_pic = QLabel()
        congrats_pic.setGeometry(10, 10, 200, 200)
        congrats_pic.setPixmap(QPixmap("./happy.png"))
        layout.addWidget(congrats_pic, 5, 0)

        self.setLayout(layout)

    def continue_task(self):
        print("@ Task Completion Menu : continue_task")
        self.parent.switch_tabs_action.setEnabled(True)
        self.parent.close_current_tab_action.setEnabled(True)
        self.parent.new_tab_action.setEnabled(True)
        self.close()

    def switch_tasks(self):
        print("@ Task Completion Menu : switch_tasks")
        self.parent.switch_tasks()
        self.close()

    def new_task(self):
        print("@ Task Completion Menu : new_task")
        self.parent.create_new_tab()
        self.close()

    def quit(self):
        print("@ Task Completion Menu : quit")
        self.parent.close_app()


# Settings menu
class SettingsMenu(QTableWidget):

    def __init__(self, parent=None):
        print("@ Settings Menu : init")
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.parent = parent
        self.setMinimumSize(self.parent.tabs.widget(0).taskMenu.width(),
                            QApplication.desktop().screen().rect().height())
        # Aligns to right
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(),
                                            QApplication.desktop().availableGeometry()))
        self.l_task_input = None
        self.m_task_input = None
        self.h_task_input = None
        self.init_ui()

    def init_ui(self):
        print("@ Settings Menu : init_ui")
        main_layout = QGridLayout()
        layout = QGridLayout()

        l_label = QLabel()
        l_label.setText("Low Intensity Task Req : ")
        layout.addWidget(l_label, 0, 0)

        self.l_task_input = QLineEdit()
        self.l_task_input.setPlaceholderText("3")
        layout.addWidget(self.l_task_input, 0, 1)

        m_label = QLabel()
        m_label.setText("Medium Intensity Task Req : ")
        layout.addWidget(m_label, 1, 0)

        self.m_task_input = QLineEdit(self)
        self.m_task_input.setPlaceholderText("5")
        layout.addWidget(self.m_task_input, 1, 1)

        h_label = QLabel()
        h_label.setText("High Intensity Task Req : ")
        layout.addWidget(h_label, 2, 0)

        self.h_task_input = QLineEdit(self)
        self.h_task_input.setPlaceholderText("7")
        layout.addWidget(self.h_task_input, 2, 1)

        close_button = QPushButton(self)
        close_button.setText("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, 4, 1)

        apply_and_close = QPushButton(self)
        apply_and_close.setText("Apply and Close")
        apply_and_close.clicked.connect(self.apply_and_close)
        layout.addWidget(apply_and_close, 5, 1)

        switch_task_button = QPushButton(self)
        switch_task_button.setText("Switch Tasks")
        switch_task_button.clicked.connect(self.switch_tasks)
        layout.addWidget(switch_task_button, 3, 0)

        new_task_button = QPushButton(self)
        new_task_button.setText("Start New Task")
        new_task_button.clicked.connect(self.new_task)
        layout.addWidget(new_task_button, 4, 0)

        quit_button = QPushButton(self)
        quit_button.setText("Quit Application")
        quit_button.clicked.connect(self.quit)
        layout.addWidget(quit_button, 5, 0)

        menu_pic = QLabel()
        menu_pic.setGeometry(10, 10, 400, 400)
        menu_pic.setPixmap(QPixmap("./whale.jpg"))

        padding = QLabel()
        padding.setGeometry(10, 10, 400, 400)

        print("Adding to main layout")
        main_layout.addWidget(menu_pic, 0, 0)
        main_layout.addLayout(layout, 1, 0)
        main_layout.addWidget(padding, 2, 0)

        print("setting")
        self.setLayout(main_layout)

    def continue_task(self):
        print("@ Task Completion Menu : continue_task")
        self.parent.switch_tabs_action.setEnabled(True)
        self.parent.close_current_tab_action.setEnabled(True)
        self.parent.new_tab_action.setEnabled(True)
        self.close()

    def switch_tasks(self):
        print("@ Settings Menu : switch_tasks")
        self.parent.switch_tasks()
        self.close()

    def new_task(self):
        print("@ Settings Menu : new_task")
        self.parent.create_new_tab()
        self.close()

    def quit(self):
        print("@ Settings Menu : quit")
        self.parent.close_app()

    def apply_and_close(self):
        print("@ Settings Menu : apply_and_close")
        try:
            self.parent.high_intensity_tasks = int(self.h_task_input.text())
            self.parent.medium_intensity_tasks = int(self.m_task_input.text())
            self.parent.light_intensity_tasks = int(self.l_task_input.text())
        except ValueError:
            print("@ Settings Menu : Value Error")
            self.parent.high_intensity_tasks = 3
            self.parent.medium_intensity_tasks = 5
            self.parent.light_intensity_tasks = 7
            self.close()
        else:
            self.close()
