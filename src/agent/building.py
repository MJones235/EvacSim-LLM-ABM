import mesa
import mesa_geo as mg
import pyproj

class Building(mg.GeoAgent):
    id: int
    
    def __init__(self, model: mesa.Model, geometry, crs: pyproj.CRS) -> None:
        super().__init__(model, geometry, crs)