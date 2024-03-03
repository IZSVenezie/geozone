from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QDialogButtonBox
from qgis.core import QgsVectorLayer

class GeoZONEEditDialog(QDialog):
    def __init__(self, layer, feature, parent=None):
        super(GeoZONEEditDialog, self).__init__(parent)
        self.layer = layer
        self.feature = feature
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)

        row = 0
        col = 0

        self.attribute_widgets = {}

        for field in self.feature.fields():
            if field.name() not in ['optype', 'uuid']:
                label = QLabel(field.name())
                line_edit = QLineEdit(str(self.feature[field.name()]))

                layout.addWidget(label, row, col)
                layout.addWidget(line_edit, row, col + 1)

                self.attribute_widgets[field.name()] = line_edit

                row += 1

                if row > 3:
                    row = 0
                    col += 2

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box, row, col)

    def get_edited_attributes(self):
        edited_attributes = {}

        for field_name, line_edit in self.attribute_widgets.items():
            edited_attributes[field_name] = line_edit.text()

        # Update the feature attributes
        for field_name, edited_value in edited_attributes.items():
            self.feature[field_name] = edited_value

        # Save the changes to the data provider of the layer
        self.layer.dataProvider().changeAttributeValues({self.feature.id(): edited_attributes})

        return edited_attributes
