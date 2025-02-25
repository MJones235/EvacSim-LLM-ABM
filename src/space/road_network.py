import networkx as nx
from sklearn.neighbors import KDTree
import pyproj
import osmnx as ox
from geopandas import GeoDataFrame
import numpy as np

class RoadNetwork:
    _nx_graph: nx.MultiDiGraph
    _kd_tree: KDTree
    _crs: pyproj.CRS
    _edges: GeoDataFrame
    _nodes: GeoDataFrame

    def __init__(self, model_crs, address: str, simulation_radius: float):
        self._crs = model_crs
        G = ox.graph_from_address(address, simulation_radius, network_type="walk")
        self.nx_graph = ox.project_graph(G, to_crs=model_crs)

    @property
    def nx_graph(self) -> nx.MultiDiGraph:
        return self._nx_graph
    
    @nx_graph.setter
    def nx_graph(self, nx_graph: nx.MultiDiGraph) -> None:
        self._nx_graph = nx_graph
        self._nodes, self._edges = ox.convert.graph_to_gdfs(nx_graph)
        self._kd_tree = KDTree(np.transpose([self.nodes.geometry.x, self.nodes.geometry.y]))

    @property
    def crs(self) -> pyproj.CRS:
        return self._crs

    @property
    def edges(self) -> GeoDataFrame:
        return self._edges
    
    @property
    def nodes(self) -> GeoDataFrame:
        return self._nodes
    