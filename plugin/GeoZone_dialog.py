from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QMessageBox
from qgis.core import QgsMessageLog, Qgis
import json
from os.path import expanduser
import os
from qgis.PyQt.QtCore import QDate

class GeoZoneDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set up the layout
        layout = QVBoxLayout()

        # Create labels and text input fields
        self.label1 = QLabel("Title *:")
        self.field1 = QLineEdit(self)

        self.label2 = QLabel("Abstract:")
        self.field2 = QLineEdit(self)

        self.label3 = QLabel("Date:")
        self.field3 = QDateEdit(self)
        self.field3.setCalendarPopup(True)  # Enables the calendar popup
        self.field3.setDate(QDate.currentDate())  # Set default date to current date

        self.label4 = QLabel("Contact *:")
        self.field4 = QLineEdit(self)

        self.label5 = QLabel("Constraints:")
        self.field5 = QLineEdit(self)

        # Create a button to confirm and store data
        self.confirm_button = QPushButton("Confirm", self)
        self.confirm_button.clicked.connect(self.confirm_and_store)
        self.confirm_button.setEnabled(False)  # Initially, disable the button

        # Add widgets to the layout
        layout.addWidget(self.label1)
        layout.addWidget(self.field1)
        layout.addWidget(self.label2)
        layout.addWidget(self.field2)
        layout.addWidget(self.label3)
        layout.addWidget(self.field3)
        layout.addWidget(self.label4)
        layout.addWidget(self.field4)
        layout.addWidget(self.label5)
        layout.addWidget(self.field5)
        layout.addWidget(self.confirm_button)

        # Set the layout for the dialog
        self.setLayout(layout)

        # Connect textChanged signals to check mandatory fields
        self.field1.textChanged.connect(self.check_mandatory_fields)
        self.field4.textChanged.connect(self.check_mandatory_fields)

    def check_mandatory_fields(self):
        # Enable the Confirm button only if fields 1 and 4 are not empty
        is_enabled = bool(self.field1.text()) and bool(self.field4.text())
        self.confirm_button.setEnabled(is_enabled)

    def confirm_and_store(self):
        # Get the user input from text fields
        data = {
            "Title": self.field1.text(),
            "Abstract": self.field2.text(),
            "Date": self.field3.date().toString("yyyy-MM-dd"),
            "Contact": self.field4.text(),
            "Constraints": self.field5.text(),
        }

        # Store data in a JSON file
        home = expanduser("~")
        home = home.replace('\\', '/')
        if not os.path.exists(home + '/GeoZone'):
            os.makedirs(home + '/GeoZone')

        
        file_path = home + "/GeoZone/metadata.json"
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=2)


        # Display a confirmation message using QMessageBox
        QMessageBox.information(self, "Confirmation", "Metadata stored successfully in {}".format(file_path))

        # Close the dialog
        self.accept()