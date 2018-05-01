#
#
#   Productivity App : Pop-up Menus
#
#   by Christopher Medrano & Zachary Mitchell
#
#
#
#

import win32gui
import win32process
import sys
import pycurl
from urllib.parse import urlencode

from PyQt5.QtWidgets import QApplication, QTableWidget, QPushButton, QGridLayout, QTextEdit, \
    QStyle, QLabel, QLineEdit, QVBoxLayout, QScrollArea, QButtonGroup, QRadioButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont


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
        self.parent.switch_tab()
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
        self.startup_folder_input = None
        self.l_task_input = None
        self.m_task_input = None
        self.h_task_input = None
        self.init_ui()

    def init_ui(self):
        print("@ Settings Menu : init_ui")
        main_layout = QGridLayout()
        layout = QGridLayout()

        startup_folder_label = QLabel()
        startup_folder_label.setText("Folder with Links:")
        layout.addWidget(startup_folder_label, 0, 0)

        self.startup_folder_input = QLineEdit()
        self.startup_folder_input.setText('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs')
        layout.addWidget(self.startup_folder_input, 0, 1)

        apply_startup_button = QPushButton(self)
        apply_startup_button.setText("Apply New Address")
        apply_startup_button.clicked.connect(self.apply_startup)
        layout.addWidget(apply_startup_button, 1, 1)

        startup_padding = QLabel()
        startup_padding.setGeometry(10, 10, 200, 30)
        layout.addWidget(startup_padding, 2, 0)

        l_label = QLabel()
        l_label.setText("Low Intensity Task Req : ")
        layout.addWidget(l_label, 3, 0)

        self.l_task_input = QLineEdit()
        self.l_task_input.setPlaceholderText("3")
        layout.addWidget(self.l_task_input, 3, 1)

        m_label = QLabel()
        m_label.setText("Medium Intensity Task Req : ")
        layout.addWidget(m_label, 4, 0)

        self.m_task_input = QLineEdit(self)
        self.m_task_input.setPlaceholderText("5")
        layout.addWidget(self.m_task_input, 4, 1)

        h_label = QLabel()
        h_label.setText("High Intensity Task Req : ")
        layout.addWidget(h_label, 5, 0)

        self.h_task_input = QLineEdit(self)
        self.h_task_input.setPlaceholderText("7")
        layout.addWidget(self.h_task_input, 5, 1)

        close_button = QPushButton(self)
        close_button.setText("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, 7, 1)

        apply_and_close = QPushButton(self)
        apply_and_close.setText("Apply and Close")
        apply_and_close.clicked.connect(self.apply_and_close)
        layout.addWidget(apply_and_close, 8, 1)

        switch_task_button = QPushButton(self)
        switch_task_button.setText("Switch Tasks")
        switch_task_button.clicked.connect(self.switch_tasks)
        layout.addWidget(switch_task_button, 6, 0)

        new_task_button = QPushButton(self)
        new_task_button.setText("Start New Task")
        new_task_button.clicked.connect(self.new_task)
        layout.addWidget(new_task_button, 7, 0)

        quit_button = QPushButton(self)
        quit_button.setText("Quit Application")
        quit_button.clicked.connect(self.quit)
        layout.addWidget(quit_button, 8, 0)

        menu_header = QLabel()
        menu_header.setText("Settings")
        menu_header.setFont(QFont("Times", 24, QFont.Bold))
        menu_header.setAlignment(Qt.AlignCenter)

        menu_pic = QLabel()
        menu_pic.setGeometry(10, 10, 400, 400)
        menu_pic.setPixmap(QPixmap("./whale.jpg"))

        padding = QLabel()
        padding.setGeometry(10, 10, 400, 400)

        print("Adding to main layout")
        main_layout.addWidget(menu_header, 0, 0)
        main_layout.addWidget(menu_pic, 1, 0)
        main_layout.addLayout(layout, 2, 0)
        main_layout.addWidget(padding, 3, 0)

        print("setting")
        self.setLayout(main_layout)

    def continue_task(self):
        print("@ Task Completion Menu : continue_task")
        self.parent.switch_tabs_action.setEnabled(True)
        self.parent.close_current_tab_action.setEnabled(True)
        self.parent.new_tab_action.setEnabled(True)
        self.parent.settings_menu_open = False
        self.close()

    def switch_tasks(self):
        print("@ Settings Menu : switch_tasks")
        self.parent.switch_tab()
        self.parent.settings_menu_open = False
        self.close()

    def new_task(self):
        print("@ Settings Menu : new_task")
        self.parent.create_new_tab()
        self.parent.settings_menu_open = False
        self.close()

    def quit(self):
        print("@ Settings Menu : quit")
        self.parent.close_app()

    def apply_startup(self):
        print("@ Settings Menu : apply_startup")
        try:
            self.parent.startup_folder = self.startup_folder_input.text()
            print("Setting to : " + self.parent.startup_folder)
        except ValueError:
            print("@ apply_startup : Value Error")
            self.parent.startup_folder = 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs'

    def apply_and_close(self):
        print("@ Settings Menu : apply_and_close")
        try:
            if len(self.h_task_input.text()) > 0:
                self.parent.high_intensity_tasks = int(self.h_task_input.text())
            if len(self.m_task_input.text()) > 0:
                self.parent.medium_intensity_tasks = int(self.m_task_input.text())
            if len(self.l_task_input.text()) > 0:
                self.parent.light_intensity_tasks = int(self.l_task_input.text())
        except ValueError:
            print("@ apply_and_close : Value Error")
            self.parent.high_intensity_tasks = 3
            self.parent.medium_intensity_tasks = 5
            self.parent.light_intensity_tasks = 7
            self.parent.settings_menu_open = False
            self.close()
        else:
            self.parent.settings_menu_open = False
            self.close()


# Recover Menu
class RecoverMenu(QTableWidget):

    def __init__(self, parent=None):
        print("@ Recover Menu : init")
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Recover Menu")
        # set to occupy size of task menu
        self.setMinimumSize(self.parent.tabs.widget(0).taskMenu.width(),
                            QApplication.desktop().screen().rect().height())
        # Aligns to right
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(),  QApplication.desktop().availableGeometry()))
        self.layout = QGridLayout()
        self.init_ui()

    def init_ui(self):
        print("@ Recover Menu : init_ui")

        title = QLabel()
        title.setText("Recovery Menu\nGrab Window")

        self.layout.addWidget(title, 0, 0)

    def add_handles(self, handles):
        print("@ Recover Menu : add_handles")
        handle_button_list = QVBoxLayout(self)
        button_scroll = QScrollArea(self)
        for i in range(len(handles)):
            if win32gui.GetWindowText(handles[i]) != "":
                handle_button = QPushButton(self)
                handle_button.setText(win32gui.GetWindowText(handles[i]))
                handle_button.clicked.connect(self.get_window_function(handles[i]))
                handle_button_list.addWidget(handle_button)
        button_scroll.setLayout(handle_button_list)
        self.layout.addWidget(button_scroll, 1, 0)
        self.setLayout(self.layout)

    def get_window_function(self, handle):
        return lambda y: self.window_function(handle)

    def window_function(self, handle):
        self.parent.tabs.widget(self.parent.tab_index).windowManager.set_to_window(handle)
        self.parent.process_ids.append(win32process.GetWindowThreadProcessId(handle))
        self.parent.recover_menu_open = False
        self.close()


class FinalSurvey(QTableWidget):

    def __init__(self, parent=None):
        print("@ Final Survey : init")
        super().__init__(parent)
        self.app_rating = 0
        self.productivity_rating = 0

        self.rating_group = None
        self.productivity_group = None

        self.comments = QTextEdit()

        self.init_ui()

    def init_ui(self):
        print("@ Final Survey : init_ui")
        self.setMinimumHeight(400)
        self.setMinimumWidth(900)
        self.move(QApplication.desktop().rect().center() - self.rect().center())

        layout = QGridLayout()

        rating_prompt = QLabel()
        rating_prompt.setText("From a scale of 1 for “why would you waste my time” to 7 for \n"
                              "“Perfection incarnate,” how was your experience with the application:")
        layout.addWidget(rating_prompt, 0, 0)

        rating_buttons = [QRadioButton(str(i+1)) for i in range(7)]
        rating_buttons[0].setChecked(True)
        self.rating_group = QButtonGroup()
        rating_group_layout = QHBoxLayout()
        for b in range(len(rating_buttons)):
            rating_group_layout.addWidget(rating_buttons[b])
            self.rating_group.addButton(rating_buttons[b])
            rating_buttons[b].clicked.connect(self.rating_set)
        layout.addLayout(rating_group_layout, 0, 1)

        productivity_prompt = QLabel()
        productivity_prompt.setText("From a -3 for “damn, it made it worse, what the fuck is this” \n"
                                    "to 3 for “Oh my God I was in the clouds, it’s better than cocaine”, \n"
                                    "how did you feel your productivity was affected through the application:")
        layout.addWidget(productivity_prompt, 1, 0)

        productivity_buttons = [QRadioButton(str(i - 3)) for i in range(7)]
        productivity_buttons[3].setChecked(True)
        self.productivity_group = QButtonGroup()
        productivity_group_layout = QHBoxLayout()
        for b in range(len(rating_buttons)):
            productivity_group_layout.addWidget(productivity_buttons[b])
            self.productivity_group.addButton(productivity_buttons[b])
            productivity_buttons[b].clicked.connect(self.productivity_set)
        layout.addLayout(productivity_group_layout, 1, 1)

        comments_prompt = QLabel()
        comments_prompt.setText("Any bugs you experienced, suggestions, comments? Write ‘em here; \n"
                                "be nice, or not, I just want an A...")
        layout.addWidget(comments_prompt, 2, 0)

        self.comments.setPlaceholderText("Enter comments here...")
        layout.addWidget(self.comments, 3, 0)

        final_picture = QLabel()
        final_picture.setPixmap(QPixmap("happy.png"))
        layout.addWidget(final_picture, 3, 1)

        submit_button = QPushButton()
        submit_button.setText("Submit")
        submit_button.clicked.connect(self.submit_survey)
        layout.addWidget(submit_button, 4, 1)

        self.setLayout(layout)

    def productivity_set(self):
        print("@ Final Survey : productivity_set")
        self.productivity_rating = self.productivity_group.checkedButton().text()

    def rating_set(self):
        print("@ Final Survey : rating_set")
        self.app_rating = self.rating_group.checkedButton().text()

    def submit_survey(self):
        print("@ Final Survey : submit_survey")

        c = pycurl.Curl()
        c.setopt(c.URL, "api.focustask.org/appreview")
        post_data = {'apprating': self.app_rating,
                     'productivityrating': self.productivity_rating,
                     'comments': self.comments.toPlainText()}
        postfields = urlencode(post_data)
        c.setopt(c.POSTFIELDS, postfields)
        c.perform()
        c.close()
        sys.exit()
