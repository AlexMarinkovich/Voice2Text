from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QHBoxLayout
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtMultimedia import QSound
from PyQt5.QtGui import QFont
from plyer import notification
import speech_recognition as sr
import pyperclip
import json 

from relative_sizes import VW

class ApplicationTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.console = QTextEdit(self)
        layout.addWidget(self.console)
        self.console.setFixedHeight(16*VW)
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background-color: rgb(40, 40, 40); color: white;")
        self.console.setFont(QFont("Consolas", 10))

        # Create a layout to horizontally align the buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout) 

        self.start_button = QPushButton("")
        button_layout.addWidget(self.start_button)
        self.start_button.setFixedSize(12*VW, 3*VW)
        self.start_button.clicked.connect(self.copy_speech)

        clear_button = QPushButton("Clear Console")
        button_layout.addWidget(clear_button)
        clear_button.setFixedSize(12*VW, 3*VW)
        clear_button.clicked.connect(lambda _: self.console.setText(""))

        # Prepare for the use of speech_recognition 
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    # handle notifications and updating the console
    def announce(self, text, notify=False, newlines=1):
        self.console.setText(self.console.toPlainText() + text + "\n"*newlines)
        if notify: notification.notify(title="Voice2Text", message=text[:256], timeout=2)
        self.console.verticalScrollBar().setValue(self.console.verticalScrollBar().maximum()) # Automatically scroll down

    def copy_speech(self):
        with open("data/settings.json", "r") as file:
            settings = json.load(file)
        
        self.announce("Say something", False)
        QCoreApplication.processEvents()

        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=3)
                text = self.recognizer.recognize_google(audio)
            
            if settings["lowercase"]: text = text.lower()
            self.announce(f"You said: {text}", False)
            
        except sr.UnknownValueError:
            self.announce("Could not understand the audio", settings["notification"], 2)
        
        except sr.WaitTimeoutError:
            self.announce("Timeout: No audio input detected", settings["notification"], 2)

        except sr.RequestError as e:
            self.announce(f"Could not request results from Google Speech Recognition service: {e}", settings["notification"], 2)

        except PermissionError:
            self.announce("Permission to access the microphone was denied", settings["notification"], 2)

        except OSError:
            self.announce("No microphone detected or microphone is not working", settings["notification"], 2)

        except Exception as e:
            self.announce(f"Error: {e}", settings["notification"], 2)
        
        else:
            with open("data/phrase_replacements.json", "r") as file:
                phrase_replacements = json.load(file)
                for phrase, replacement in phrase_replacements:
                    text = text.replace(phrase, replacement)
            
            pyperclip.copy(text)
            self.announce(f"Copied: {text}", settings["notification"], 2)
            if settings["sound"]: QSound.play('data/sound.wav')

        