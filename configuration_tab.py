from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import json

from relative_sizes import VW

class ConfigurationTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table_widget = QTableWidget()  
        self.layout.addWidget(self.table_widget)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Phrase", "Replacement", ""])
        
        # Adjust the sizing of the table
        self.table_widget.verticalHeader().setFixedWidth(1.2*VW)
        self.table_widget.setColumnWidth(0, 15*VW)
        self.table_widget.setColumnWidth(1, 15*VW)
        self.table_widget.setColumnWidth(2, 2.5*VW)

        # Make the headers non-selectable
        self.table_widget.horizontalHeader().sectionPressed.disconnect()
        self.table_widget.verticalHeader().sectionPressed.disconnect()
        
        # Set the table to have no horizontal scrolling
        self.table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.add_entry_button = QPushButton("Add New Phrase")
        self.layout.addWidget(self.add_entry_button)
        self.add_entry_button.setFixedHeight(2*VW)
        self.add_entry_button.clicked.connect(self.add_entry)

        # Save the configuration to the json file when the table is edited
        self.table_widget.itemChanged.connect(self.save_config)

        # Load the configuration from the json file
        self.load_config()

    def add_entry(self, phrase="", replacement=""):
        row_number = self.table_widget.rowCount()
        self.table_widget.insertRow(row_number)
        self.table_widget.setItem(row_number, 0, QTableWidgetItem(phrase))
        self.table_widget.setItem(row_number, 1, QTableWidgetItem(replacement))
        
        # Create a delete button and connect it to the delete_entry method
        delete_button = QPushButton("✖")
        delete_button.clicked.connect(self.delete_entry)
        self.table_widget.setCellWidget(row_number, 2, delete_button)

        # Automically scroll down
        self.table_widget.verticalScrollBar().setValue(self.table_widget.verticalScrollBar().maximum())

    def delete_entry(self):
        selected_indexes = self.table_widget.selectedIndexes()
        if not selected_indexes: return

        row_number = selected_indexes[0].row()
        self.table_widget.removeRow(row_number)
        
        # Automically scroll down
        self.table_widget.verticalScrollBar().setValue(self.table_widget.verticalScrollBar().maximum())

        # Save the configuration to the json file when an entry is deleted
        self.save_config()

    def save_config(self):
        phrase_replacements = []
        for row in range(self.table_widget.rowCount()):
            phrase = self.table_widget.item(row, 0)
            replacement = self.table_widget.item(row, 1)
            if phrase and replacement:
                phrase_replacements.append([phrase.text(), replacement.text()])
        
        with open("data/phrase_replacements.json", "w") as file:
            json.dump(phrase_replacements, file)

    def load_config(self):
        with open("data/phrase_replacements.json", "r") as file:
            phrase_replacements = json.load(file)
            for phrase, replacement in phrase_replacements:
                self.add_entry(phrase, replacement)