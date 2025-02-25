import mesa
import mesa_geo as mg

from ..space.road_network import RoadNetwork
from ..space.city import City
from ..space.buildings import Buildings
from ..agent.geo_agents import Road
from ..agent.building import Building

class EvacuationModel(mesa.Model):
    roads: RoadNetwork
    space: City
    buildings: Buildings

    def __init__(
        self,  
        address: str,
        simulation_radius: float,
        model_crs="epsg:27700"
    ) -> None:
        super().__init__()

        self.space = City(model_crs)

        self.roads = RoadNetwork(model_crs, address, simulation_radius)
        self.space.add_agents(mg.AgentCreator(Road, self).from_GeoDataFrame(self.roads.edges))

        self.buildings = Buildings(model_crs, address, simulation_radius)
        self.space.add_agents(mg.AgentCreator(Building, self).from_GeoDataFrame(self.buildings.df))

    def step(self) -> None:
        super().step()
        