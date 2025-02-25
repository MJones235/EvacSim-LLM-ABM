import mesa_geo as mg
import mesa
import pyproj
from shapely.geometry import Point

class Road(mg.GeoAgent):

    def __init__(self, model: mesa.Model, geometry: Point, crs: pyproj.CRS):
        super().__init__(model, geometry, crs)