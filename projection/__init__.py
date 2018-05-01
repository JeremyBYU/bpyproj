"""
This file is apart of bpyproj - A blender addon to allow GIS Map Projections
Copyright (C) 2018, Jeremy Castagno
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
import logging
from pyproj import Proj

DEFAULT_SRID = 'EPSG:3857'
DEFAULT_PROJ_PARAMS = 'EPSG:'

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class GeneralProjection:
    """Class that allows conversion between geodetic and any planar coordinate system
    """

    def __init__(self, srid=DEFAULT_SRID, proj_params=DEFAULT_PROJ_PARAMS, **kwargs):
        # setting default values
        self.lat = 0.  # in degrees
        self.lon = 0.  # in degrees

        # override default lat long coordinates
        for attr in kwargs:
            setattr(self, attr, kwargs[attr])
        # Set up user defined projection
        try:
            if proj_params:
                self.proj = Proj(projparams=proj_params)
            else:
                self.proj = Proj(init=srid)
        except:
            log.error('SRID is invalid! Defaulting to %s', DEFAULT_SRID)
            self.proj = Proj(init=DEFAULT_SRID)

        self.offset = self.proj(self.lon, self.lat)

    def update_projection(self, srid):
        """Updates the projected coordinate system

        Arguments:
            srid {SRID} -- Unique identifier for spatial reference system
        """
        try:
            self.proj = Proj(init=srid)
        except:
            log.error('SRID is invalid! Defaulting to %s', DEFAULT_SRID)
            self.proj = Proj(init=DEFAULT_SRID)

        self.offset = self.proj(self.lon, self.lat)

    def fromGeographic(self, lat, lon):
        """Converts lat long to a projected planar coordinate system

        Arguments:
            lat {number} -- latitude
            lon {number} -- longitude
        """
        proj_coords = self.proj(lon, lat)
        return (proj_coords[0] - self.offset[0], proj_coords[1] - self.offset[1], 0.)

    def toGeographic(self, x, y):
        """Converts planar coordinate system to projected coordinate system

        Arguments:
            x {number} -- x coordinate
            y {number} -- y coordinate
        """
        lonlat_coords = self.proj(
            x + self.offset[0], y + self.offset[1], inverse=True)
        return (lonlat_coords[1], lonlat_coords[0])
