# 🌍 GeoZONE
GeoZONE - a QGIS python plugin allowing to track zones with specific animal diseases


## GeoZONE Plugin for QGIS

The GeoZONE plugin is a tool designed for QGIS users to streamline the management of geographic zones within spatial data. This plugin simplifies tasks related to creating, editing, and storing information about geographic zones, such as disease outbreak areas, wildlife habitats, or quarantine zones.

## Features

### 1. GeoZONE Layer Management

The plugin introduces a dedicated layer, GeoZONE_Layer, to manage geographic zones efficiently. If the layer doesn't exist, the plugin creates an empty one or loads an existing layer at a default location.

### 2. Copying Selected Geometries

Users can easily copy selected geometries from other layers to the GeoZONE_Layer. This feature is useful for aggregating specific geographic zones into a centralized layer.

### 3. Metadata Entry

The plugin prompts users to provide metadata for each saved GeoZONE_Layer. Metadata includes essential attributes like operation type, country code, local identifier, and accuracy. Users can also add additional metadata fields as needed.

### 4. Custom Dialog for Editing Attributes

When selecting features from the GeoZONE_Layer, the plugin now displays a custom dialog for each feature. This dialog allows users to modify attributes, excluding 'optype' and 'uuid', providing a more intuitive editing experience.

### 5. Zip File Export

After saving the GeoZONE_Layer and its metadata, the plugin conveniently zips all related files (shapefile, metadata JSON, etc.) into a single zip file. This helps users maintain a tidy and organized folder structure for their geographic zone data.

## How to Use

1. **Installation:**
   - Clone the [GeoZONE repository](https://github.com/yourusername/GeoZONE) to your local machine.

2. **Activate the Plugin:**
   - Open QGIS and navigate to the Plugins menu.
   - Click on Manage and Install Plugins.
   - Browse to the GeoZONE plugin and activate it.

3. **Accessing GeoZONE:**
   - Once activated, find the GeoZONE plugin under the Plugins menu.

4. **Creating and Managing GeoZONE_Layer:**
   - Click on GeoZONE to access the plugin.
   - Follow the prompts to create or manage the GeoZONE_Layer.

5. **Copying and Editing Features:**
   - Select features from other layers and copy them to GeoZONE_Layer.
   - Edit attributes using the custom dialog for selected features in GeoZONE_Layer.

6. **Saving and Exporting:**
   - Save GeoZONE_Layer and metadata.
   - Files are automatically zipped into a neat archive for easy storage.

## Known Issues

- Currently, users may encounter an issue with the visual layout of the attribute editing dialog. This will be addressed in future updates.

## Contributing

We welcome contributions and feedback! If you encounter issues or have suggestions, please submit them through the [issue tracker](https://github.com/yourusername/GeoZONE/issues).

Happy mapping! 🗺️✨
