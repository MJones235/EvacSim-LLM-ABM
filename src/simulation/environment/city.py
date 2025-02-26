import mesa_geo as mg

class City(mg.GeoSpace):

    def __init__(self, crs: str):
        super().__init__(crs)