#
#
#   Productivity App
#
#   by Christopher Medrano & Zachary Mitchell
#
#
#

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLineEdit, QLayout
from PyQt5.QtCore import Qt, pyqtSlot


class TaskMenu(QWidget):

    def __init__(self, parent=None):
        print("@ tm : init")
        super().__init__(parent)
        self.parent = parent
        self.title = 'Task Menu Prototype'
        self.totalTasksCompleted = 0
        self.tasksCompleted = 0
        self.taskList = []
        self.taskIndex = 2
        self.textBox = QLineEdit(self)
        self.taskLayout = QGridLayout()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        # self.setStyleSheet("background-color:cyan")
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
        self.taskLayout.addLayout(button_layout, 0, 0)
        self.taskLayout.addWidget(self.textBox, 1, 0)
        self.taskLayout.setAlignment(Qt.AlignTop)
        self.setLayout(self.taskLayout)
        self.show()

    @pyqtSlot()
    def add_task(self):
        print("@ tm : add_task")
        text = self.textBox.text()
        if len(text) > 0:
            new_button = QPushButton(self)
            new_button.setFlat(True)
            new_button.setText(text)
            new_button.clicked.connect(lambda: self.complete_task(new_button))
            self.taskLayout.addWidget(new_button, self.taskIndex, 0)
            self.taskIndex += 1

    @pyqtSlot(QPushButton)
    def complete_task(self, button):
        print("@ tm : complete_task")
        if '\u0336' not in button.text():
            button.setText('\u0336'.join(button.text()) + '\u0336')
            self.totalTasksCompleted += 1
            self.tasksCompleted += 1
        else:
            print("Already completed Task")

    def remove_last_task(self):
        print("@ tm : remove_last_task")
        if self.taskLayout.count() > 2:
            self.taskIndex -= 1
            self.taskLayout.itemAt(self.taskLayout.count()-1).widget().deleteLater()

    def clear_tasks(self):
        print("@ tm : clear_tasks")
        self.taskIndex = 2
        if self.taskLayout.count() > 2:
            for i in range(self.taskLayout.count()-1, 1, -1):
                self.taskLayout.itemAt(i).widget().deleteLater()

