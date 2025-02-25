import networkx as nx
from sklearn.neighbors import KDTree
import pyproj
import osmnx as ox
from geopandas import GeoDataFrame

class Buildings:
    _crs: pyproj.CRS
    _df: GeoDataFrame

    def __init__(self, model_crs, address: str, simulation_radius: float):
        self._crs = model_crs
        df = ox.features_from_address(address, {'building': True}, simulation_radius)
        df.geometry = df.geometry.to_crs(model_crs)
        self._df = df

    @property
    def df(self) -> GeoDataFrame:
        return self._df