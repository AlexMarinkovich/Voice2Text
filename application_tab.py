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

    def copy_speech(self):
        with open("settings.json", "r") as file:
            settings = json.load(file)

        recognizer = sr.Recognizer()

        if self.console.toPlainText(): self.console.setText(f"{self.console.toPlainText()}\n\nSay something")
        else: self.console.setText("Say something")
        self.console.verticalScrollBar().setValue(self.console.verticalScrollBar().maximum()) # Automatically scroll down

        QCoreApplication.processEvents()

        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)
                if settings["lowercase"]: text = text.lower()
                self.console.setText(f"{self.console.toPlainText()}\nYou said: {text}")
            
            except sr.UnknownValueError:
                error_message = "Could not understand the audio"
                self.console.setText(f"{self.console.toPlainText()}\n{error_message}")
                if settings["notification"]: notification.notify(title="Voice2Text", message=error_message, timeout=2)
                return
            
            except sr.RequestError as e:
                error_message = f"Could not request results from Google Speech Recognition service: {e}"
                self.console.setText(f"{self.console.toPlainText()}\n{error_message}")
                if settings["notification"]: notification.notify(title="Voice2Text", message=error_message[:256], timeout=2)
                return

        except PermissionError:
            error_message = "Permission to access the microphone was denied"
            self.console.setText(f"{self.console.toPlainText()}\n{error_message}")
            if settings["notification"]: notification.notify(title="Voice2Text", message=error_message, timeout=2)
            return

        except OSError:
            error_message = "No microphone detected or microphone is not working"
            self.console.setText(f"{self.console.toPlainText()}\n{error_message}")
            if settings["notification"]: notification.notify(title="Voice2Text", message=error_message, timeout=2)
            return

        except Exception as e:
            error_message = f"Error: {e}"
            self.console.setText(f"{self.console.toPlainText()}\n{error_message}")
            if settings["notification"]: notification.notify(title="Voice2Text", message=error_message[:256], timeout=2)
            return

        with open("phrase_replacements.json", "r") as file:
            phrase_replacements = json.load(file)
            for phrase, replacement in phrase_replacements:
                text = text.replace(phrase, replacement)
        

        copy_message = f"Copied: {text}"

        pyperclip.copy(text)
        self.console.setText(f"{self.console.toPlainText()}\n{copy_message}")
        self.console.verticalScrollBar().setValue(self.console.verticalScrollBar().maximum()) # Automatically scroll down
        
        if settings["sound"]: QSound.play('sound.wav')
        if settings["notification"]: notification.notify(title="Voice2Text", message=copy_message[:256], timeout=2)

        