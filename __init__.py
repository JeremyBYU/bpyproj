"""
This file is apart of bpyproj - A blender addon to allow GIS Map Projections
Copyright (C) 2018 Jeremy Castagno
jeremybyu@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import sys
import textwrap
import logging

import bpy

log = logging.getLogger(__name__)
print(__name__)


bl_info = {
    "name": "Map Projection",
    "author": "Jeremy Castagno <jeremybyu@gmail.com>",
    "version": (1, 0, 0),
    "blender": (2, 7, 9),
    "location": "File > Import > OpenStreetMap (.osm)",
    "description": "Specify a map projection for external import plugins (e.g. blender-osm)",
    "warning": "",
    "wiki_url": "https://github.com/JeremyBYU/bpyproj",
    "tracker_url": "https://github.com/JeremyBYU/bpyproj/issues",
    "support": "COMMUNITY",
    "category": "Import-Export",
}


# force cleanup of sys.modules to avoid conflicts with the other addons for Blender
# for m in [
#         "app", "building", "gui", "manager", "material", "parse", "realistic", "overlay",
#         "renderer", "terrain", "util", "defs", "setup"
#     ]:
#     sys.modules.pop(m, 0)


def _checkPath():
    path = os.path.dirname(__file__)
    if path in sys.path:
        sys.path.remove(path)
    # make <path> the first one to search for a module
    sys.path.insert(0, path)


_checkPath()

import projection # pylint: disable=I0011, C0413
from dependencies import install_deps, get_python_path  # pylint: disable=I0011, C0413


class InstallDependencies(bpy.types.Operator):
    bl_idname = "bpyproj.dependencies"
    bl_label = "Install Dependencies"
    bl_description = "Install Pip and Pyproj dependencies"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def invoke(self, context, event):
        install_deps()
        return {'FINISHED'}


class PyprojProperties(bpy.types.PropertyGroup):
    """Specifies global properties available for this module
    """

    srid = bpy.props.StringProperty(
        name="SRID",
        description="Spatial Reference System ID (e.g. EPSG:3857)",
        default='EPSG:3857'
    )


class PanelSettings(bpy.types.Panel):
    """Creates a GUI panel to allow user to specify SRID projection

    """
    bl_label = "Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "projection"

    def draw(self, context):
        """Draws the panel

        Arguments:
            context {object} -- Context of the invocation

        """

        layout = self.layout
        addon = context.scene.bpyproj

        box = layout.box()
        box.prop(addon, "srid")

        box.operator("bpyproj.dependencies")


def register():
    """Registers this addon modules
    """
    bpy.utils.register_module(__name__)
    bpy.types.Scene.bpyproj = bpy.props.PointerProperty(type=PyprojProperties)


def unregister():
    """Unregister this addon modules
    """
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.bpyproj


if __name__ == "__main__":
    register()
