#
#
#   Productivity App
#
#   by Christopher Medrano & Zachary Mitchell
#
#
#

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLineEdit, QLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSlot


class TaskMenu(QWidget):

    def __init__(self, parent=None):
        print("@ tm : init")
        super().__init__(parent)
        self.parent = parent
        self.title = 'Task Menu'
        self.window_opened = False
        self.tasks_to_completion = -1
        self.total_tasks_completed = 0
        self.tasks_completed = 0
        self.taskList = []
        self.taskIndex = 3
        self.textBox = QLineEdit(self)
        self.textBox.returnPressed.connect(self.add_task)
        self.task_stats = QLabel()
        self.taskLayout = QGridLayout()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        # self.setStyleSheet("background-color:cyan")
        self.taskLayout.addWidget(self.task_stats, 0, 0)
        self.task_stats.setText("Tasks Completed : " + str(self.tasks_completed))
        button_layout = QGridLayout()
        add_task_button = QPushButton(self)
        add_task_button.setText("Add Task")
        add_task_button.clicked.connect(self.add_task)
        button_layout.addWidget(add_task_button, 0, 0)
        remove_task_button = QPushButton(self)
        remove_task_button.setText("Remove Last Task")
        remove_task_button.clicked.connect(self.remove_last_task)
        button_layout.addWidget(remove_task_button, 0,1)
        clear_tasks_button = QPushButton(self)
        clear_tasks_button.setText("Clear Tasks")
        clear_tasks_button.clicked.connect(self.clear_tasks)
        button_layout.addWidget(clear_tasks_button, 0, 2)
        button_layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.taskLayout.addLayout(button_layout, 1, 0)
        self.taskLayout.addWidget(self.textBox, 2, 0)
        self.taskLayout.setAlignment(Qt.AlignTop)
        self.setLayout(self.taskLayout)
        self.show()

    @pyqtSlot()
    def add_task(self):
        # prevent repeat tasks, or empty tasks from being made into buttons
        print("@ tm : add_task")
        text = self.textBox.text()
        if len(text) > 0 and self.window_opened:
            if self.taskLayout.count() == 3:
                new_button = QPushButton(self)
                new_button.setFlat(True)
                new_button.setText(text)
                new_button.clicked.connect(lambda: self.complete_task(new_button))
                self.taskLayout.addWidget(new_button, self.taskIndex, 0)
                self.textBox.setText("")
                self.taskIndex += 1
            else:
                if text != self.taskLayout.itemAt(self.taskLayout.count()-1).widget().text():
                    new_button = QPushButton(self)
                    new_button.setFlat(True)
                    new_button.setText(text)
                    new_button.clicked.connect(lambda: self.complete_task(new_button))
                    self.taskLayout.addWidget(new_button, self.taskIndex, 0)
                    self.textBox.setText("")
                    self.taskIndex += 1
            if self.taskIndex - 3 == self.tasks_to_completion:
                self.parent.set_enable_window(True)

    @pyqtSlot(QPushButton)
    def complete_task(self, button):
        print("@ tm : complete_task")
        if '\u0336' not in button.text():
            button.setText('\u0336'.join(button.text()) + '\u0336')
            self.total_tasks_completed += 1
            self.tasks_completed += 1
            self.task_stats.setText("Tasks Completed : " + str(self.tasks_completed))
            if self.tasks_completed == self.tasks_to_completion:
                self.prompt_all_tasks_completed()
                self.tasks_completed = 0
        else:
            print("Already completed Task")

    def remove_last_task(self):
        print("@ tm : remove_last_task")
        if self.taskLayout.count() > 3:
            self.taskIndex -= 1
            self.taskLayout.itemAt(self.taskLayout.count()-1).widget().deleteLater()

    def clear_tasks(self):
        print("@ tm : clear_tasks")
        self.taskIndex = 3
        if self.taskLayout.count() > 3:
            for i in range(self.taskLayout.count()-1, 1, -1):
                self.taskLayout.itemAt(i).widget().deleteLater()

    def set_tasks_till_completion(self, task_num):
        print("@ tm : set_tasks_till_completion")
        self.tasks_to_completion = task_num

    def prompt_all_tasks_completed(self):
        print("@ tm : prompt_all_tasks_completed")
        self.parent.parent.complete()

    def set_window_opened(self, opened):
        print("@ tm : set_window_opened")
        self.window_opened = opened
