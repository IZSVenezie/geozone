from qgis.PyQt.QtGui import QIcon
from PyQt5.QtCore import QVariant, QSettings
from qgis.PyQt.QtWidgets import QAction, QMenu, QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton
from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsProject, QgsField, QgsFields, QgsVectorFileWriter, QgsMessageLog, Qgis, QgsFeature, QgsMapLayerStyle
from .GeoZONE_dialog import GeoZONEDialog
from .GeoZONEEditDialog import GeoZONEEditDialog
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
        self.setWindowTitle("GeoZONE")
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


class GeoZONE:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        # Create a menu entry if it doesn't exist
        self.menu = self.iface.mainWindow().findChild(QMenu, '&GeoZONE')
        if not self.menu:
            self.menu = QMenu('&GeoZONE', self.iface.mainWindow().menuBar())
            self.iface.mainWindow().menuBar().addMenu(self.menu)

        icon_path = 'logo.png'

        self.action = QAction(QIcon(icon_path), "GeoZONE", self.iface.mainWindow())
        self.action.triggered.connect(self.run_plugin)
        self.menu.addAction(self.action)



    def unload(self):
        # Cleanup code goes here
        pass

    def run_plugin(self):
        flag = 0
        # Check if GeoZONE_Layer exists, if not, create it
        existing_layers = QgsProject.instance().mapLayersByName("GeoZONE_Layer")
        if not existing_layers:
            flag = 2
            self.create_empty_layer()

        # Get the GeoZONE_Layer
        geozone_layer = QgsProject.instance().mapLayersByName("GeoZONE_Layer")[0]

        geozone_layer.startEditing()
        for feature in geozone_layer.getFeatures():
            if not feature["optype"]:
                feature["optype"] = "INSERT"
                #
                geozone_layer.updateFeature(feature)
        geozone_layer.commitChanges()        
        
        # Iterate through all opened layers
        for layer_id, layer in QgsProject.instance().mapLayers().items():
            if isinstance(layer, QgsRasterLayer): 
                pass
            else:
                # Skip GeoZONE_Layer itself
                if layer_id == geozone_layer.id():
                    # Check if geometries from the GeoZONE_Layer are selected
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
                    # If geometries are selected, copy them to GeoZONE_Layer
                    self.copy_selected_geometries(geozone_layer, selected_features)

        # If no geometry is selected, save the GeoZONE_Layer and prompt for metadata
        #if not geozone_layer.selectedFeatures():
        if flag == 0:
            QMessageBox.information(None, "Information", "No operation performed. Select the feature you want to edit or the features you want to export in order to continue.")
            #old save_layer_with_metadata callpoint (was exporting all GeoZONE features)
            

    
    
    ################################################ LOAD GEOZONE (load/create db shp) ###############################################

    def create_empty_layer(self):
        # Default location for GeoZONE_Layer
        layer = None
        home = expanduser("~")
        default_layer_path = os.path.join(home, 'geozone.shp')

        existing_layers = QgsProject.instance().mapLayersByName("GeoZONE_Layer")

        if existing_layers:
            # GeoZONE_Layer already exists, open it
            layer = existing_layers[0]
        elif os.path.exists(default_layer_path):
            # GeoZONE_Layer not loaded, but exists at default position, load it
            layer = QgsVectorLayer(default_layer_path, "GeoZONE_Layer", "ogr")
            if not layer.isValid():
                QMessageBox.critical(None, "Error", "Error loading the GeoZONE_Layer. Please check the file.")
                QgsMessageLog.logMessage("Error loading the GeoZONE_Layer", "GeoZONE", Qgis.Critical)
                return
        else:
            # GeoZONE_Layer not loaded and not found at default position, create an empty layer
            layer_name = "GeoZONE_Layer"
            layer_type = "Polygon"
            crs = "EPSG:4326"

            # Create a new vector layer with specified fields
            layer = QgsVectorLayer(f"{layer_type}?crs={crs}&index=yes", layer_name, "memory")
            if not layer.isValid():
                QMessageBox.critical(None, "Error", "Error creating the GeoZONE_Layer. Please check the parameters.")
                QgsMessageLog.logMessage("Error creating the GeoZONE_Layer", "GeoZONE", Qgis.Critical)
                return

            # Define the fields to add
            fields = QgsFields()
            field_names = ["optype", "uuid", "localid", "geoname", "accuracy",
                        "zonetype", "subtype", "status", "datebegin", "dateend", "disease", "countryf",
                        "s_avian", "s_bee", "s_bovine", "s_equine", "s_lago", "s_sh_go",
                        "s_swine", "s_other", "s_wild", "m_dest", "m_surv_w", "m_surv_o",
                        "m_trace", "m_stpout", "m_zoning", "m_movctrl", "m_quarant",
                        "m_vectctrl", "m_selkill", "m_screen", "m_vacc"]

            field_types = [QVariant.String] * 8 + [QVariant.Date, QVariant.Date] + [QVariant.String, QVariant.String] + [QVariant.Int] * 21
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
        QgsMessageLog.logMessage("GeoZONE_Layer opened successfully.", "GeoZONE", Qgis.Info)
        QMessageBox.information(None, "Information", "GeoZONE_Layer opened successfully.")



    ################################################ IMPORT GEOMETRIES (from other layers) ###############################################

    def copy_selected_geometries(self, layer, selected_features):
        # Check if GeoZONE_Layer exists, if not, create it
        existing_layers = QgsProject.instance().mapLayersByName("GeoZONE_Layer")
        if not existing_layers:
            self.create_empty_layer()

        # Get the GeoZONE_Layer
        geozone_layer = QgsProject.instance().mapLayersByName("GeoZONE_Layer")[0]

        # Add selected features to GeoZONE_Layer
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
            if layer.name() != "GeoZONE_Layer":
                QgsProject.instance().removeMapLayer(layer)

        QgsMessageLog.logMessage("Selected geometries copied to GeoZONE_Layer", "GeoZONE", Qgis.Info)
        QMessageBox.information(None, "Information", "Selected geometries copied to GeoZONE_Layer.")



    ################################################ SAVE LAYER (selected geometries) ###############################################

    def save_layer_with_metadata(self, layer, flag):
        # Save the layer to the specified path
        current_timestamp = datetime.now()
        formatted_timestamp = current_timestamp.strftime('%Y%m%d_%H%M%S')
        home = expanduser("~")
        if not os.path.exists(home + '/GeoZONE'):
            os.makedirs(home + '/GeoZONE')
        save_path = home + "/GeoZONE/GeoZONE" + formatted_timestamp + ".shp"

        QgsVectorFileWriter.writeAsVectorFormat(layer, save_path, "utf-8", layer.crs(), "ESRI Shapefile", onlySelected = True)

        # Display a confirmation message
        QgsMessageLog.logMessage("Layer saved successfully to {}".format(save_path), "GeoZONE", Qgis.Info)

        
        # Prompt for metadata and save to JSON
        plugin_dialog = GeoZONEDialog()
        result = plugin_dialog.exec_()

        if result == QDialog.Accepted:
            files_to_zip = [home + "/GeoZONE/GeoZONE" + formatted_timestamp + ".shp", home + "/GeoZONE/GeoZONE" + formatted_timestamp + ".shx", home + "/GeoZONE/GeoZONE" + formatted_timestamp + ".cpg", home + "/GeoZONE/GeoZONE" + formatted_timestamp + ".dbf", home + "/GeoZONE/GeoZONE" + formatted_timestamp + ".prj", home + "/GeoZONE/metadata.json"]
            zip_filename = home + "/GeoZONE/GeoZONE" + formatted_timestamp + ".zip"

            with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                for file_to_zip in files_to_zip:
                    if os.path.exists(file_to_zip):
                        zip_file.write(file_to_zip, os.path.basename(file_to_zip))
                        QgsMessageLog.logMessage(f'{file_to_zip} added to {zip_filename}')
                        os.remove(file_to_zip)
                    else:
                        QgsMessageLog.logMessage(f'Warning: {file_to_zip} not found, skipping.')
            
            target_folder = os.path.dirname(os.path.abspath(zip_filename))

            # Update optype field of each feature to "noaction"
            layer.startEditing()
            for feature in layer.selectedFeatures():
                layer.changeAttributeValue(feature.id(), layer.fields().indexFromName("optype"), "noaction")
            layer.commitChanges()
            
            # Get the current operating system
            current_os = platform.system()

            # Define the command to open the folder based on the operating system
            if current_os == 'Windows':
                command = ['explorer', target_folder]
            elif current_os == 'Linux':
                command = ['xdg-open', target_folder]
            else:
                print(f'Unsupported operating system: {current_os}')
                exit()

            # Execute the command
            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError:
                print(f'Failed to open the folder. Please navigate to {target_folder} manually.')
        
        else:
            QMessageBox.information(None, "Information", "Metadata information box not filled. Exporting process has been blocked.")


    #################################### EDIT DIALOG ###############################
            
    #def edit_attributes_dialog(self, layer, selected_features):
    #    for feature in selected_features:
    #        dialog = GeoZONEEditDialog(layer, feature)
      #      result = dialog.exec_()

     #       if result == QDialog.Accepted:
      #          edited_attributes = dialog.get_edited_attributes()
       #         QgsMessageLog.logMessage(f"Attributes edited: {edited_attributes}", "GeoZONE", Qgis.Info)
       #         self.update_feature_attributes(feature, edited_attributes, layer)

    def edit_attributes_dialog(self, layer, selected_features):
        for feature in selected_features:
            # Get the existing attribute values of the feature
            existing_attributes = feature.attributes()
            # Convert the existing attribute values to a dictionary using field names as keys
            existing_attributes_dict = {field.name(): value for field, value in zip(layer.fields(), existing_attributes)}
            
            # Pass the existing attribute values to the edit dialog
            dialog = GeoZONEEditDialog(layer, feature, existing_attributes_dict)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                edited_attributes = dialog.get_edited_attributes()
                QgsMessageLog.logMessage(f"Attributes edited: {edited_attributes}", "GeoZONE", Qgis.Info)
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