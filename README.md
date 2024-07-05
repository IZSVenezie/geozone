# 🌍 GeoZone
GeoZone - a QGIS python plugin allowing to track zones with specific animal diseases


## GeoZone Plugin for QGIS

The GeoZone plugin is a tool designed for QGIS users to streamline the management of geographic zones within spatial data. This plugin simplifies tasks related to creating, editing, and storing information about geographic zones, such as disease outbreak areas, wildlife habitats, or quarantine zones.

## Features

### 1. GeoZone Layer Management

The plugin introduces a dedicated layer, GeoZone_Layer, to manage geographic zones efficiently. If the layer doesn't exist, the plugin creates an empty one or loads an existing layer at a default location.

### 2. Copying Selected Geometries

Users can easily copy selected geometries from other layers to the GeoZone_Layer. This feature is useful for aggregating specific geographic zones into a centralized layer.

### 3. Metadata Entry

The plugin prompts users to provide metadata for each saved GeoZone_Layer. Metadata includes essential attributes like operation type, country code, local identifier, and accuracy. Users can also add additional metadata fields as needed.

### 4. Custom Dialog for Editing Attributes

When selecting features from the GeoZone_Layer, the plugin now displays a custom dialog for each feature. This dialog allows users to modify attributes, excluding 'optype' and 'uuid', providing a more intuitive editing experience.

### 5. Zip File Export

After saving the GeoZone_Layer and its metadata, the plugin conveniently zips all related files (shapefile, metadata JSON, etc.) into a single zip file. This helps users maintain a tidy and organized folder structure for their geographic zone data.

## How to Use

1. **Installation:**
   - Clone the [GeoZone repository](https://github.com/yourusername/GeoZone) to your local machine.

2. **Activate the Plugin:**
   - Open QGIS and navigate to the Plugins menu.
   - Click on Manage and Install Plugins.
   - Browse to the GeoZone plugin and activate it.

3. **Accessing GeoZone:**
   - Once activated, find the GeoZone plugin under the Plugins menu.

4. **Creating and Managing GeoZone_Layer:**
   - Click on GeoZone to access the plugin.
   - Follow the prompts to create or manage the GeoZone_Layer.

5. **Copying and Editing Features:**
   - Select features from other layers and copy them to GeoZone_Layer.
   - Edit attributes using the custom dialog for selected features in GeoZone_Layer.

6. **Saving and Exporting:**
   - Save GeoZone_Layer and metadata.
   - Files are automatically zipped into a neat archive for easy storage.

## Known Issues

- Currently, users may encounter an issue with the visual layout of the attribute editing dialog. This will be addressed in future updates.

## Contributors
   - [Mirco Cazzaro](https://github.com/mircocazzaro)
   - Giacomo De Conti
   - [Alberto Tomasin](https://github.com/therealtoma)
   - Rodrigo Macario
   - [Matteo Mazzucato](https://github.com/mmazzucato)
   - Federica Sbettega
   - Nicola Ferrè

## Contributing

We welcome contributions and feedback! If you encounter issues or have suggestions, please submit them through the [issue tracker](https://github.com/yourusername/GeoZone/issues).

Happy mapping! 🗺️✨