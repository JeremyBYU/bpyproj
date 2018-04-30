# Blender Map Projection Plugin

This plugin registers a module in the blender python environment which can perform arbitrary Map Projections. The plugin makes use of [pyproj](https://github.com/jswhit/pyproj) in order to perform these projections. To learn more about projections and why the are useful, I encourage you to read [this](http://desktop.arcgis.com/en/arcmap/10.3/guide-books/map-projections/what-are-map-projections.htm#GUID-57EBA564-3106-4CD0-94AB-FA43C1320523).


Pyproj relies upon a binary dependency, [proj4](http://proj4.org/), requiring this plugin to distribute these binaries. This plugin will attempt to install these binaries into the blender embedded python environment.

## Install Procedure

Download the plugin (this repository) and extract to your plugin folder.  Another way is by following these [instructions](https://blendersensei.com/definitive-guide-to-installing-blender-addons/) using the Blenders built in GUI to install the plugin zip file.


## How to Use

### Install Dependencies

Install dependencies by clicking the button `Install Dependencies`. If it was a success a message will pop up letting you know. If a failure occurs a message box will pop up providing instructions. Note special instruction for windows follow.

Windows:

For the first launch, please run Blender as **administrator** so that the dependencies can be installed. This is necessary because blender is installed in `C:\Programs Files` which is off limits without administrator privilege.

If blender is **not** run with administrator privilege (possibly because you are uncomfortable giving it permissions for this **one** install), then a message box will present itself telling the user what files need to be copied manually with administrative privilege. 

### Set SRID

Spatial Reference Identifier (SRID) is a code that tells the plugin which projection system you desire to work with. A list of common SRIDS can be found here at [EPSG.io](http://epsg.io/). Type in your code and then click the button `Set Projection`.






