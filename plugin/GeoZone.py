from qgis.PyQt.QtGui import QIcon
from PyQt5.QtCore import QVariant
from qgis.PyQt.QtWidgets import QAction, QMenu, QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton
from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsProject, QgsField, QgsFields, QgsVectorFileWriter, QgsMessageLog, Qgis, QgsFeature
from .GeoZone_dialog import GeoZoneDialog
from .GeoZoneEditDialog import GeoZoneEditDialog
from os.path import expanduser
import os
import time
import zipfile
import subprocess
import platform
from datetime import datetime
import hashlib

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super(CustomDialog, self).__init__(parent)
        self.setWindowTitle("GeoZone")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("You have selected just one feature. Select the action you want to perform:"))
        edit_button = QPushButton("Edit Attributes", self)
        edit_button.clicked.connect(self.edit_attributes)
        layout.addWidget(edit_button)
        export_button = QPushButton("Export Feature", self)
        export_button.clicked.connect(self.export_feature)
        layout.addWidget(export_button)

    def edit_attributes(self):
        self.result = "edit"
        self.accept()

    def export_feature(self):
        self.result = "export"
        self.accept()


class GeoZone:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        # Create a menu entry if it doesn't exist
        self.menu = self.iface.mainWindow().findChild(QMenu, '&GeoZone')
        if not self.menu:
            self.menu = QMenu('&GeoZone', self.iface.mainWindow().menuBar())
            self.iface.mainWindow().menuBar().addMenu(self.menu)

        icon_path = 'logo.png'

        self.action = QAction(QIcon(icon_path), "GeoZone", self.iface.mainWindow())
        self.action.triggered.connect(self.run_plugin)
        self.menu.addAction(self.action)



    def unload(self):
        # Cleanup code goes here
        pass

    def run_plugin(self):
        flag = 0
        # Check if GeoZone_Layer exists, if not, create it
        existing_layers = QgsProject.instance().mapLayersByName("GeoZone_Layer")
        if not existing_layers:
            flag = 2
            self.create_empty_layer()

        # Get the GeoZone_Layer
        geozone_layer = QgsProject.instance().mapLayersByName("GeoZone_Layer")[0]

        geozone_layer.startEditing()
        for feature in geozone_layer.getFeatures():
            if not feature["optype"]:
                feature["optype"] = "INSERT"
                for field in ["s_avian", "s_bee", "s_bovine", "s_equine", "s_lago", "s_sh_go", "s_swine", "s_other", "s_wild", "m_stmout", "m_mov", "m_biosec", "m_vactrt", "m_animid", "m_antrace", "m_ctrace", "m_surv", "m_aware"]:
                    feature[field] = 0
                geozone_layer.updateFeature(feature)
        geozone_layer.commitChanges()        
        
        # Iterate through all opened layers
        for layer_id, layer in QgsProject.instance().mapLayers().items():
            if isinstance(layer, QgsRasterLayer): 
                pass
            else:
                # Skip GeoZone_Layer itself
                if layer_id == geozone_layer.id():
                    # Check if geometries from the GeoZone_Layer are selected
                    selected_features = geozone_layer.selectedFeatures()
                    if selected_features:
                        flag = 1
                        if len(selected_features) == 1:
                            dialog = CustomDialog(None)
                            if dialog.exec_() == QDialog.Accepted:
                                if dialog.result == "edit":
                                    # User chose to edit attributes
                                    self.edit_attributes_dialog(geozone_layer, selected_features)
                                elif dialog.result == "export":
                                    # User chose to export the selected feature
                                    self.save_layer_with_metadata(geozone_layer, flag)
                            # Prompt custom dialog for editing attributes
                        else:
                            self.save_layer_with_metadata(geozone_layer, flag)
                    continue

                # Get selected features from each layer
                selected_features = layer.selectedFeatures()

                if selected_features:
                    flag = 1
                    # If geometries are selected, copy them to GeoZone_Layer
                    self.copy_selected_geometries(geozone_layer, selected_features)

        # If no geometry is selected, save the GeoZone_Layer and prompt for metadata
        #if not geozone_layer.selectedFeatures():
        if flag == 0:
            QMessageBox.information(None, "Information", "No operation performed. Select the feature you want to edit or the features you want to export in order to continue.")
            #old save_layer_with_metadata callpoint (was exporting all GeoZone features)
            

    
    
    ################################################ LOAD GEOZONE (load/create db shp) ###############################################

    def create_empty_layer(self):
        # Default location for GeoZone_Layer
        layer = None
        home = expanduser("~")
        default_layer_path = os.path.join(home, 'geozone.shp')

        existing_layers = QgsProject.instance().mapLayersByName("GeoZone_Layer")

        if existing_layers:
            # GeoZone_Layer already exists, open it
            layer = existing_layers[0]
        elif os.path.exists(default_layer_path):
            # GeoZone_Layer not loaded, but exists at default position, load it
            layer = QgsVectorLayer(default_layer_path, "GeoZone_Layer", "ogr")
            if not layer.isValid():
                QMessageBox.critical(None, "Error", "Error loading the GeoZone_Layer. Please check the file.")
                QgsMessageLog.logMessage("Error loading the GeoZone_Layer", "GeoZone", Qgis.Critical)
                return
        else:
            # GeoZone_Layer not loaded and not found at default position, create an empty layer
            layer_name = "GeoZone_Layer"
            layer_type = "Polygon"
            crs = "EPSG:4326"

            # Create a new vector layer with specified fields
            layer = QgsVectorLayer(f"{layer_type}?crs={crs}&index=yes", layer_name, "memory")
            if not layer.isValid():
                QMessageBox.critical(None, "Error", "Error creating the GeoZone_Layer. Please check the parameters.")
                QgsMessageLog.logMessage("Error creating the GeoZone_Layer", "GeoZone", Qgis.Critical)
                return

            # Define the fields to add
            fields = QgsFields()
            field_names = ["optype", "uuid", "localid", "geoname", "accuracy",
                        "zonetype", "subtype", "status", "datebegin", "dateend", "disease", "countryf",
                        "s_avian", "s_bee", "s_bovine", "s_equine", "s_lago", "s_sh_go",
                        "s_swine", "s_other", "s_wild", "m_stmout", "m_mov", "m_biosec", "m_vactrt", "m_animid", "m_antrace", "m_ctrace", "m_surv", "m_aware"]

            field_types = [QVariant.String] * 8 + [QVariant.Date, QVariant.Date] + [QVariant.String, QVariant.String] + [QVariant.Int] * 18
            field_lengths = [10, 36, 50, 250, 50, 100, 50, 50, 10, 10, 100, 150]
            i = 0

            for field_name, field_type in zip(field_names, field_types):
                field = QgsField(field_name, field_type, len=field_lengths[i]) if field_type == QVariant.String or field_type == QVariant.Date else QgsField(field_name, field_type, len=1)
                fields.append(field)
                i += 1

            # Add the fields to the layer
            layer.dataProvider().addAttributes(fields)
            layer.updateFields()

            # Save the layer to the default position
            QgsVectorFileWriter.writeAsVectorFormat(layer, default_layer_path, "utf-8", layer.crs(), "ESRI Shapefile")


        sld_path = os.path.join(os.path.dirname(__file__), "sld_geozone.sld")
        layer.loadSldStyle(sld_path)


        # Add the layer to the map canvas
        QgsProject.instance().addMapLayer(layer)

        # Log and show a confirmation message
        QgsMessageLog.logMessage("GeoZone_Layer opened successfully.", "GeoZone", Qgis.Info)
        QMessageBox.information(None, "Information", "GeoZone_Layer opened successfully.")



    ################################################ IMPORT GEOMETRIES (from other layers) ###############################################

    def copy_selected_geometries(self, layer, selected_features):
        # Check if GeoZone_Layer exists, if not, create it
        existing_layers = QgsProject.instance().mapLayersByName("GeoZone_Layer")
        if not existing_layers:
            self.create_empty_layer()

        # Get the GeoZone_Layer
        geozone_layer = QgsProject.instance().mapLayersByName("GeoZone_Layer")[0]

        # Add selected features to GeoZone_Layer
        geozone_layer.startEditing()
        geozone_layer_data = geozone_layer.dataProvider()

        for feature in selected_features:
            new_feature = QgsFeature(layer.fields())
            new_feature.setGeometry(feature.geometry())
            #new_feature.setAttributes(feature.attributes())
            new_feature["optype"] = "INSERT"
            new_feature["uuid"] = "" #str(uuid.uuid4())
            new_feature["localid"] = ""
            geozone_layer_data.addFeature(new_feature)

        geozone_layer.commitChanges()

        for layer_id, layer in QgsProject.instance().mapLayers().items():
            if layer.name() != "GeoZone_Layer":
                QgsProject.instance().removeMapLayer(layer)

        QgsMessageLog.logMessage("Selected geometries copied to GeoZone_Layer", "GeoZone", Qgis.Info)
        QMessageBox.information(None, "Information", "Selected geometries copied to GeoZone_Layer.")



    ################################################ SAVE LAYER (selected geometries) ###############################################

    def save_layer_with_metadata(self, layer, flag):
        # Define mandatory fields
        mandatory_fields = ['localid', 'zonetype', 'datebegin', 'disease']  # Adjust field names as necessary

        # Check if all mandatory fields are correctly set
        all_fields_valid = True
        country = ""
        for feature in layer.selectedFeatures():
            country = feature["countryf"]
            for field_name in mandatory_fields:
                if not feature[field_name] or feature[field_name] in [None, "", "Invalid"]:  # Adjust invalid conditions as needed
                    all_fields_valid = False
                    break
            if not all_fields_valid:
                break

        if not all_fields_valid:
            QMessageBox.warning(None, "Missing Data", "Not all mandatory fields are set for some of the selected geometries.")
            return
        
        # Proceed with additional processing if layer saved successfully
        plugin_dialog = GeoZoneDialog()
        result = plugin_dialog.exec_()
        if result == QDialog.Accepted:

            # Proceed if all fields are valid
            current_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            home = expanduser("~")
            directory_path = os.path.join(home, 'GeoZone')
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            save_path = os.path.join(directory_path, f"GeoZone{current_timestamp}.shp")

            QgsVectorFileWriter.writeAsVectorFormat(layer, save_path, "utf-8", layer.crs(), "ESRI Shapefile", onlySelected=True)
            QgsMessageLog.logMessage(f"Layer saved successfully to {save_path}", "GeoZone", Qgis.Info)

            # Assume metadata is saved to a JSON file as part of GeoZoneDialog processing
            metadata_file = os.path.join(directory_path, "metadata.json")
            files_to_zip = [save_path, f"{save_path[:-4]}.shx", f"{save_path[:-4]}.dbf", f"{save_path[:-4]}.prj", f"{save_path[:-4]}.cpg", metadata_file]
            zip_filename = os.path.join(directory_path, f"{country}_GeoZone{current_timestamp}.zip")

            with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                for file_path in files_to_zip:
                    if os.path.exists(file_path):
                        zip_file.write(file_path, os.path.basename(file_path))
                        QgsMessageLog.logMessage(f"{file_path} added to {zip_filename}", "GeoZone")
                        os.remove(file_path)
                    else:
                        QgsMessageLog.logMessage(f"Warning: {file_path} not found, skipping.", "GeoZone")

            # Open the folder containing the zip file
            target_folder = os.path.dirname(os.path.abspath(zip_filename))
            self.open_folder_command(target_folder)
        else:
            QMessageBox.warning(None, "Information", "Metadata information box not filled. Exporting process has been blocked.")

    def open_folder_command(self, target_folder):
        current_os = platform.system()
        command_map = {
            'Windows': ['explorer', target_folder],
            'Linux': ['xdg-open', target_folder],
            'Darwin': ['open', target_folder]  # macOS
        }
        command = command_map.get(current_os)
        if command:
            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError:
                pass
        else:
            QMessageBox.warning(None, "Unsupported OS", f"Unsupported operating system: {current_os}")


    #################################### EDIT DIALOG ###############################
            
    #def edit_attributes_dialog(self, layer, selected_features):
    #    for feature in selected_features:
    #        dialog = GeoZoneEditDialog(layer, feature)
      #      result = dialog.exec_()

     #       if result == QDialog.Accepted:
      #          edited_attributes = dialog.get_edited_attributes()
       #         QgsMessageLog.logMessage(f"Attributes edited: {edited_attributes}", "GeoZone", Qgis.Info)
       #         self.update_feature_attributes(feature, edited_attributes, layer)

    def edit_attributes_dialog(self, layer, selected_features):
        for feature in selected_features:
            # Get the existing attribute values of the feature
            existing_attributes = feature.attributes()
            # Convert the existing attribute values to a dictionary using field names as keys
            existing_attributes_dict = {field.name(): value for field, value in zip(layer.fields(), existing_attributes)}
            
            # Pass the existing attribute values to the edit dialog
            dialog = GeoZoneEditDialog(layer, feature, existing_attributes_dict)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                edited_attributes = dialog.get_edited_attributes()
                QgsMessageLog.logMessage(f"Attributes edited: {edited_attributes}", "GeoZone", Qgis.Info)
                self.update_feature_attributes(feature, edited_attributes, layer)


    def update_feature_attributes(self, feature, edited_attributes, layer):
        # Start editing the layer
        layer.startEditing()

        # Update the attributes of the feature
        for key, value in edited_attributes.items():
            feature[key] = value

        

        if feature["optype"] != "INSERT":
            feature["optype"] = "UPDATE"
        
        feature["uuid"] = self.generate_uuid4_string(str(feature["localid"]) + str(feature["countryf"]) + str(feature["zonetype"]) + str(feature["disease"]))
        
        # Update the feature in the data provider
        layer.updateFeature(feature)

        # Commit the changes to the data provider
        layer.commitChanges()

        # Update the layer's fields
        layer.updateFields()

    ##########################################
        
    def generate_uuid4_string(self, string):
        # Generate MD5 hash of the input string

        hash_string = string + str(int(time.time()))
        hash = hashlib.md5(hash_string.encode()).hexdigest()
        
        # Construct the UUID4 string
        uuid4 = f"{hash[:8]}-" \
                f"{hash[8:12]}-" \
                f"{hash[12:15]}-" \
                f"{hex(int(hash[16], 16) & 0x3 | 0x8)[2]}{hash[17:20]}-" \
                f"{hash[20:32]}"
        
        return uuid4