"""
ID: Iso_Study.py 
Date: 2024-08-11
Author: Kosta F
"""

"""
Goal: Allow users to isolate their env to focus on their school goals within a time period.
      Distractions will be limited and when the user attempts to procrastinate they will be reminded of their goals.
      A set time frame can be implemented by the user and a force quit option is available in case of emergencies.
      This is targeted to students who wish to study productively.
"""

import AppOpener as AO
import psutil
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

# Global variables
silencedApps = []
tasks = []
force_quit = False

# Default silenced apps that can be changed to be any list of apps 
DEFAULT_SILENCED_APPS = ["Steam", "Riot", "Discord", "Minecraft"]

# Monitors silenced apps to make sure none are open during the time limit
def silence_apps():
    """Silences all applications in the silencedApps list."""
    for app in silencedApps:
        AO.close(app, output=False)

def monitor_apps():
    """Monitors running applications and closes any silenced apps if reopened."""
    running_apps = [proc.name() for proc in psutil.process_iter(['name'])] 
    for app in silencedApps:
        for running_app in running_apps:
            if app.lower() in running_app.lower():
                AO.close(app, output=False)

# Pop up IsoStudy window
class IsoStudyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initializes the UI components."""
        self.setWindowTitle("Iso-Study Setup")
        self.setGeometry(300, 100, 400, 300)

        layout = QtWidgets.QVBoxLayout()
        
        self.time_label = QtWidgets.QLabel("Set your countdown: HH:MM:SS")
        layout.addWidget(self.time_label)

        time_layout = QtWidgets.QHBoxLayout()
        self.hours_input = QtWidgets.QLineEdit("00")
        self.hours_input.setValidator(QtGui.QIntValidator(0, 23))
        time_layout.addWidget(self.hours_input)
        time_layout.addWidget(QtWidgets.QLabel(":"))

        self.minutes_input = QtWidgets.QLineEdit("00")
        self.minutes_input.setValidator(QtGui.QIntValidator(0, 59))
        time_layout.addWidget(self.minutes_input)
        time_layout.addWidget(QtWidgets.QLabel(":"))

        self.seconds_input = QtWidgets.QLineEdit("00")
        self.seconds_input.setValidator(QtGui.QIntValidator(0, 59))
        time_layout.addWidget(self.seconds_input)

        layout.addLayout(time_layout)

        self.app_label = QtWidgets.QLabel("Add applications to silence (press Enter after each):")
        layout.addWidget(self.app_label)

        self.app_input = QtWidgets.QLineEdit()
        self.app_input.returnPressed.connect(self.add_silenced_app)
        layout.addWidget(self.app_input)

        self.app_list = QtWidgets.QListWidget()
        self.app_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.app_list.customContextMenuRequested.connect(self.show_app_context_menu)
        layout.addWidget(self.app_list)

        self.default_button = QtWidgets.QPushButton('Use Default Silenced Apps')
        self.default_button.clicked.connect(self.use_default_apps)
        layout.addWidget(self.default_button)

        self.task_label = QtWidgets.QLabel("Add tasks to complete (press Enter after each):")
        layout.addWidget(self.task_label)

        self.task_input = QtWidgets.QLineEdit()
        self.task_input.returnPressed.connect(self.add_task)
        layout.addWidget(self.task_input)

        self.task_list = QtWidgets.QListWidget()
        self.task_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.task_list.customContextMenuRequested.connect(self.show_task_context_menu)
        layout.addWidget(self.task_list)

        self.start_button = QtWidgets.QPushButton('Start')
        self.start_button.clicked.connect(self.start_isolation)
        layout.addWidget(self.start_button)

        self.setLayout(layout)
        self.show()

    def add_silenced_app(self):
        app = self.app_input.text().strip()
        if app:
            self.app_list.addItem(app)
            silencedApps.append(app)
            self.app_input.clear()

    def use_default_apps(self):
        self.app_list.clear()
        silencedApps.clear()
        for app in DEFAULT_SILENCED_APPS:
            self.app_list.addItem(app)
            silencedApps.append(app)

    def show_app_context_menu(self, position):
        menu = QtWidgets.QMenu()
        remove_action = menu.addAction("Remove")
        action = menu.exec_(self.app_list.viewport().mapToGlobal(position))
        if action == remove_action:
            selected_item = self.app_list.currentItem()
            if selected_item:
                silencedApps.remove(selected_item.text())
                self.app_list.takeItem(self.app_list.row(selected_item))

    def add_task(self):
        task = self.task_input.text().strip()
        if task:
            self.task_list.addItem(task)
            tasks.append(task)
            self.task_input.clear()

    def show_task_context_menu(self, position):
        menu = QtWidgets.QMenu()
        remove_action = menu.addAction("Remove")
        action = menu.exec_(self.task_list.viewport().mapToGlobal(position))
        if action == remove_action:
            selected_item = self.task_list.currentItem()
            if selected_item:
                tasks.remove(selected_item.text())
                self.task_list.takeItem(self.task_list.row(selected_item))

    def start_isolation(self):
        global force_quit
        force_quit = False

        hours = int(self.hours_input.text())
        minutes = int(self.minutes_input.text())
        seconds = int(self.seconds_input.text())

        if hours == 0 and minutes == 0 and seconds == 0:
            QtWidgets.QMessageBox.warning(self, "Invalid Time", "Please set a valid countdown time.")
            return

        silence_apps()

        self.reminder_window = TaskReminder(hours, minutes, seconds)
        self.reminder_window.show()

# Task and Timer Pop up window
class TaskReminder(QtWidgets.QWidget):
    def __init__(self, hours, minutes, seconds):
        super().__init__()
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.init_ui()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.start_countdown()
        self.zen_mode = False 

    def init_ui(self):
        """Initializes the UI components."""
        self.setWindowTitle("Task Reminder")
        self.setGeometry(300, 100, 400, 300)

        self.task_layout = QtWidgets.QVBoxLayout()

        self.task_label = QtWidgets.QLabel("<b>Tasks to do:</b>")
        self.task_layout.addWidget(self.task_label)

        self.task_checkboxes = []
        for task in tasks:
            checkbox = QtWidgets.QCheckBox(task)
            self.task_layout.addWidget(checkbox)
            self.task_checkboxes.append(checkbox)

        self.countdown_label = QtWidgets.QLabel(f"Time Remaining: {self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}")
        self.task_layout.addWidget(self.countdown_label)

        self.zen_mode_button = QtWidgets.QPushButton('Zen Mode')
        self.zen_mode_button.clicked.connect(self.toggle_zen_mode)
        self.task_layout.addWidget(self.zen_mode_button)

        self.exit_button = QtWidgets.QPushButton('End Session Early')
        self.exit_button.clicked.connect(self.force_quit)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(self.task_layout)
        vbox.addWidget(self.exit_button)
        self.setLayout(vbox)

    def toggle_zen_mode(self):
        self.zen_mode = not self.zen_mode
        if self.zen_mode:
            for checkbox in self.task_checkboxes:
                checkbox.setVisible(False)
            self.task_label.setVisible(False)
            self.resize(300, 150)
        else:
            for checkbox in self.task_checkboxes:
                checkbox.setVisible(True)
            self.task_label.setVisible(True)
            self.resize(400, 300)

    def update_countdown(self):
        if self.seconds > 0:
            self.seconds -= 1
        elif self.minutes > 0:
            self.minutes -= 1
            self.seconds = 59
        elif self.hours > 0:
            self.hours -= 1
            self.minutes = 59
            self.seconds = 59

        self.countdown_label.setText(f"Time Remaining: {self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}")

        if self.hours == 0 and self.minutes == 0 and self.seconds == 0:
            self.timer.stop()

    def start_countdown(self):
        self.timer.start(1000) 

    def force_quit(self):
        global force_quit
        force_quit = True
        self.timer.stop()
        self.close()

def StudyApp():
    app = QtWidgets.QApplication(sys.argv)
    study_app = IsoStudyApp()
    sys.exit(app.exec_())

if __name__ == "__main__":
    StudyApp()
