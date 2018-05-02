# Blender Map Projection Plugin

This plugin registers a module in the blender python environment which can perform arbitrary Map Projections. The plugin makes use of [pyproj](https://github.com/jswhit/pyproj) in order to perform these projections. To learn more about projections and why the are useful, I encourage you to read [this](http://desktop.arcgis.com/en/arcmap/10.3/guide-books/map-projections/what-are-map-projections.htm#GUID-57EBA564-3106-4CD0-94AB-FA43C1320523).


Pyproj relies upon a binary dependency, [Proj4](http://proj4.org/), requiring this plugin to distribute these binaries. This plugin will attempt to install these binaries into the blender embedded python environment.

## Install Procedure

Download the plugin (this repository) and extract to your plugin folder.  Another way is by following these [instructions](https://blendersensei.com/definitive-guide-to-installing-blender-addons/) using the Blenders built in GUI to install the plugin zip file.

### Install Dependencies

After installation you will **also** need to install *dependencies* for the plugin.  You can do this by going to File -> User Preferences -> Add-ons.  Then scroll to the `Import-Export: Map Projection` (this plugin) and expand the plugin by clicking the arrow. You should see a section titled `Preferences` along with a button. Install dependencies by clicking the button `Install Dependencies` (see picture below). If it was a success a message will appear letting you know. If a failure occurs a message box will pop up providing details (also look at the log output). Note special instruction for Windows OS follow.

![Settings](imgs/dependencies.png)

Windows:

For the first launch, please run Blender as **administrator** so that the dependencies can be installed. This is necessary because blender is installed in `C:\Programs Files` which is off limits without administrator privilege.

If blender is **not** run with administrator privilege (possibly because you are uncomfortable giving it permissions for this **one** install), then the log provides instructions detailing what files need to be copied manually with administrative privilege. 


## How to Use


Spatial Reference Identifier (SRID) is a code that tells the plugin which projection system you desire to work with. A list of common SRID's can be found here at [EPSG.io](http://epsg.io/). Simply type in the SRID (e.g. EPSG:3857) into the `SRID` field.

![Settings](imgs/settings.png)

 If more granular control is needed you can change the drop down menu (`Specify Projection`) from `SRID` to `Proj4 Params`. You can now input the Proj.4 parameter string directly in the field titled `Proj4 Parameters`.

![Settings](imgs/settings_proj4.png)








