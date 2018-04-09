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
        super().__init__(parent)
        self.title = 'Task Menu Prototype'
        self.totalTasksCompleted = 0
        self.tasksCompleted = 0
        self.taskList = []
        self.taskIndex = 2
        self.textBox = QLineEdit(self)
        self.taskLayout = QGridLayout()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setStyleSheet("background-color:cyan")
        buttonLayout = QGridLayout()
        self.addTaskButton = QPushButton(self)
        self.addTaskButton.setText("Add Task")
        self.addTaskButton.clicked.connect(self.addTask)
        buttonLayout.addWidget(self.addTaskButton, 0, 0)
        self.removeTaskButton = QPushButton(self)
        self.removeTaskButton.setText("Remove Last Task")
        self.removeTaskButton.clicked.connect(self.removeLastTask)
        buttonLayout.addWidget(self.removeTaskButton, 0,1)
        self.clearTasksButton = QPushButton(self)
        self.clearTasksButton.setText("Clear Tasks")
        self.clearTasksButton.clicked.connect(self.clearTasks)
        buttonLayout.addWidget(self.clearTasksButton, 0, 2)
        buttonLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.taskLayout.addLayout(buttonLayout, 0, 0)
        self.taskLayout.addWidget(self.textBox, 1, 0)
        self.taskLayout.setAlignment(Qt.AlignTop)
        self.setLayout(self.taskLayout)
        self.show()

    @pyqtSlot()
    def addTask(self):
        text = self.textBox.text()
        if len(text) > 0:
            new_button = QPushButton(self)
            new_button.setFlat(True)
            new_button.setText(text)
            new_button.clicked.connect(self.completeTask)
            self.taskLayout.addWidget(new_button, self.taskIndex, 0)
            self.taskIndex += 1
            print("Adding Task : " + text)

    @pyqtSlot(QPushButton)
    def completeTask(self, button):
        button.setText('\u0336'.join(button.text()) + '\u0336')
        self.totalTasksCompleted += 1
        self.tasksCompleted += 1
        print("completed task: " + button.text())

    def removeLastTask(self):
        if self.taskLayout.count() > 2:
            self.taskIndex -= 1
            self.taskLayout.itemAt(self.taskLayout.count()-1).widget().deleteLater()

    def clearTasks(self):
        self.taskIndex = 2
        if self.taskLayout.count() > 2:
            for i in range(self.taskLayout.count()-1, 1, -1):
                self.taskLayout.itemAt(i).widget().deleteLater()

