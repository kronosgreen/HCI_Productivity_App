#
#
#   Productivity App : Pop-up Menus
#
#   by Christopher Medrano & Zachary Mitchell
#
#
#
#

from PyQt5.QtWidgets import QApplication, QTableWidget, QPushButton, QGridLayout, QStyle
from PyQt5.QtCore import Qt


class TabTable(QTableWidget):

    def __init__(self, parent=None):
        print("@ tab menu : init")
        super().__init__(parent)
        self.parent = parent
        self.setMinimumSize(600, 600)
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())

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
        self.close()


class IntensityMenu(QTableWidget):

    def __init__(self, parent=None):
        print("@ Intensity Menu : init")
        super().__init__(parent)
        self.setWindowTitle("Set Task Intensity")
        self.parent = parent
        self.setMinimumSize(400, QApplication.desktop().screen().rect().height())
        # Aligns to right
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(),
                                            QApplication.desktop().availableGeometry()))
        # Center Aligns
        # self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.add_intensity_buttons()

    def add_intensity_buttons(self):
        print("@ Intensity Menu : add_intensity_buttons")
        intensity_nums = self.parent.get_intensities()
        intensities = ["Light Intensity " + str(intensity_nums[0]),
                       "Medium Intensity " + str(intensity_nums[1]),
                       "High Intensity " + str(intensity_nums[2])]
        layout = QGridLayout()
        for i in range(len(intensities)):
            intensity_button = QPushButton(self)
            intensity_button.setText(intensities[i])
            intensity_button.clicked.connect(self.create_intensity_function(intensity_nums[i]))
            layout.addWidget(intensity_button, i, 0)
        self.setLayout(layout)

    def create_intensity_function(self, x):
        print("@ Intensity Menu : create_intensity_function")
        return lambda y: self.set_intensity(x)

    def set_intensity(self, x):
        self.parent.tabs.widget(self.parent.tabs.currentIndex()).set_intensity(x)
        self.close()
