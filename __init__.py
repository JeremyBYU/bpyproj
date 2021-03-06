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
import logging

import bpy  # pylint: disable=E0401

log = logging.getLogger(__name__)

bl_info = {
    "name": "Map Projection (bpyproj)",
    "author": "Jeremy Castagno <jeremybyu@gmail.com>",
    "version": (1, 0, 3),
    "blender": (2, 80, 0),
    "location": "On the GUI panel of external import addons (e.g. blender-osm)",
    "description": "Specify a map projection for external import addons (e.g. blender-osm)",
    "warning": "",
    "wiki_url": "https://github.com/JeremyBYU/bpyproj",
    "tracker_url": "https://github.com/JeremyBYU/bpyproj/issues",
    "support": "COMMUNITY",
    "category": "Import-Export",
}


def _checkPath():
    path = os.path.dirname(__file__)
    if path in sys.path:
        sys.path.remove(path)
    # make <path> the first one to search for a module
    sys.path.insert(0, path)


_checkPath()

from dependencies import install_deps  # pylint: disable=I0011, C0413


def getProjection(lat, lon):
    """Returns an instantiated GeneralProjection Class

    Arguments:
        lat {number} -- origin latitude
        lon {number} -- origin longitude
    """
    # Attempt to import GeneralProjection module
    # Will fail if dependencies not installed
    try:
        from projection import GeneralProjection
        log.info('Returning requested GeneralProjection')

        srid = bpy.context.scene.bpyproj.srid
        proj_params = bpy.context.scene.bpyproj.proj_params
        # srid and proj4 params are blank, return None
        if not srid and not proj_params:
            log.info(
                'No projection selected by user. Returning None to calling function')
            return None
        # Ensure that proj params are not set if user selects SRID
        if bpy.context.scene.bpyproj.proj_type == 'srid':
            proj_params = ''

        return GeneralProjection(srid=srid, proj_params=proj_params, lat=lat, lon=lon)
    except Exception as e:
        log.error(
            'Dependencies not installed for bpyproj! Please install dependencies')
        log.error('Error: %s', e)
        return None


def draw(context, layout):
    """Specifies the GUI elements to be drawn by an external plugin

    Arguments:
        context {} -- Blender Context
        layout {} -- GUI layout
    """
    addon = context.scene.bpyproj
    box = layout.box()

    box.prop(addon, "proj_type")
    if addon.proj_type == "srid":
        box.prop(addon, "srid")
    else:
        box.prop(addon, "proj_params")
    # box.operator("bpyproj.dependencies")


class PyprojProperties(bpy.types.PropertyGroup):
    """Specifies global properties available for this module
    """

    proj_type = bpy.props.EnumProperty(
        name="Specify Projection",
        items=(
            ("srid", "SRID",
                "Use Spatial Reference System Identifier (e.g. EPSG:3857)"),
            ("params", "Proj4 Params",
                "Specify the Proj4 parameters as a string")
        ),
        description="Specify Projection with SRID or Proj4 parameter string ",
        default="srid"
    )
    srid = bpy.props.StringProperty(
        name="SRID",
        description="Spatial Reference System ID (e.g. EPSG:3857)",
        default=''
    )
    proj_params = bpy.props.StringProperty(
        name="Proj4 Parameters",
        description="Proj4 Projection Parameters",
        default=''
    )


def register():
    """Registers this addon modules
    """
    install_deps()
    bpy.utils.register_class(PyprojProperties)
    bpy.types.Scene.bpyproj = bpy.props.PointerProperty(type=PyprojProperties)


def unregister():
    """Unregister this addon modules
    """
    bpy.utils.unregister_class(PyprojProperties)
    del bpy.types.Scene.bpyproj


if __name__ == "__main__":
    register()
