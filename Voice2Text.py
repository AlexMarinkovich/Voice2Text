import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt5.QtCore import QTimer
import keyboard

from application_tab import ApplicationTab
from configuration_tab import ConfigurationTab
from settings_tab import SettingsTab
from relative_sizes import VW

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(36*VW, 24*VW)
        self.setWindowTitle("Voice2Text")

        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        # Create and add tabs
        self.application_tab = ApplicationTab()
        self.central_widget.addTab(self.application_tab, 'Application')
        self.configuration_tab = ConfigurationTab()
        self.central_widget.addTab(self.configuration_tab, 'Configuration')
        self.settings_tab = SettingsTab()
        self.central_widget.addTab(self.settings_tab, 'Settings')

        # Make the keybind only work when the application tab is open
        self.central_widget.currentChanged.connect(self.tab_changed)
        self.tab_changed(0) # This is ran because the application tab is opened on start up
        
    def tab_changed(self, tab_number):
        if tab_number == 0:
            hotkey = self.settings_tab.set_hotkey_button.text()
            self.application_tab.start_button.setText(f"Start ({hotkey})")
            keyboard.on_press_key(hotkey, lambda _: QTimer.singleShot(0, self.application_tab.copy_speech))
        else:
            keyboard.unhook_all()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())