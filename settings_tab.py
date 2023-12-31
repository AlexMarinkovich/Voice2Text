from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QPushButton, QSlider
from PyQt5.QtCore import Qt, QRect
import keyboard
import json

from relative_sizes import VW

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Align the hotkey setting and its text horizontally 
        hotkey_layout = QHBoxLayout()
        layout.addLayout(hotkey_layout)
        hotkey_layout.setAlignment(Qt.AlignLeft)

        hotkey_layout.addWidget(QLabel("Start hotkey:"))
        self.set_hotkey_button = QPushButton()
        hotkey_layout.addWidget(self.set_hotkey_button)
        self.set_hotkey_button.setFixedSize(6*VW, 2*VW)
        self.set_hotkey_button.clicked.connect(self.capture_key)


        self.lowercase_checkbox = QCheckBox("Convert text to lowercase.")
        layout.addWidget(self.lowercase_checkbox)
        self.lowercase_checkbox.stateChanged.connect(self.save_settings)


        self.notification_checkbox = QCheckBox("Notify me when speech is copied.")
        layout.addWidget(self.notification_checkbox)
        self.notification_checkbox.stateChanged.connect(self.save_settings)


        self.sound_checkbox = QCheckBox("Play sound when speech is copied.")
        layout.addWidget(self.sound_checkbox)
        self.sound_checkbox.stateChanged.connect(self.save_settings)


        # Align the mic sensivity slider and its text horizontally
        slider_layout = QHBoxLayout()
        slider_layout.setContentsMargins(0, 0, 3*VW, 0)
        layout.addLayout(slider_layout)
        
        self.slider_percentage = QLabel()
        slider_layout.addWidget(self.slider_percentage)

        self.mic_sens_slider = QSlider(Qt.Horizontal)
        slider_layout.addWidget(self.mic_sens_slider)
        self.mic_sens_slider.setRange(50, 200)
        self.mic_sens_slider.valueChanged.connect(self.save_settings)
        self.mic_sens_slider.valueChanged.connect(lambda _: self.slider_percentage.setText(f"Microphone Sensitivity:   {self.mic_sens_slider.value()}%"))

        
        # Load settings from the json file
        self.load_settings()

    def capture_key(self):
        self.set_hotkey_button.setText("Press any key...")
        keyboard.on_press(self.on_key_press)
    
    def on_key_press(self, event):
        self.set_hotkey_button.setText(event.name)
        self.save_settings()
        keyboard.unhook_all()

    def save_settings(self):
        settings = {"hotkey": self.set_hotkey_button.text(), 
                    "lowercase": self.lowercase_checkbox.isChecked(),
                    "notification": self.notification_checkbox.isChecked(), 
                    "sound": self.sound_checkbox.isChecked(),
                    "mic_sensitivity": self.mic_sens_slider.value()}
        with open("data/settings.json", "w") as file:
            json.dump(settings, file)
    
    def load_settings(self):
        with open("data/settings.json", "r") as file:
            settings = json.load(file)
            self.set_hotkey_button.setText(settings["hotkey"])
            self.lowercase_checkbox.setChecked(settings["lowercase"])
            self.notification_checkbox.setChecked(settings["notification"])
            self.sound_checkbox.setChecked(settings["sound"])
            self.slider_percentage.setText(f"Microphone Sensitivity:   {settings['mic_sensitivity']}%")
            self.mic_sens_slider.setValue(settings["mic_sensitivity"])