from typing import Any
import mesa
import mesa_geo as mg
import datetime

from src.services.llm_service import LLMService
from src.services.osm_service import OSMService

from ..agents.person import Person

from ..environment.road_network import RoadNetwork
from ..environment.city import City
from ..environment.buildings import Buildings
from ..agents.geo_agents import Road
from ..agents.building import Building

class EvacuationModel(mesa.Model):
    roads: RoadNetwork
    space: City
    buildings: Buildings
    crs: str
    time: datetime
    address: str

    llm_service: LLMService
    osm_service: OSMService

    def __init__(
        self,  
        address: str,
        simulation_radius: float,
        population: dict[str, Any],
        start_time: datetime,
        model_crs: str,
    ) -> None:
        super().__init__()

        self.llm_service = LLMService()
        self.osm_service = OSMService()

        self.crs = model_crs
        self.time = start_time
        self.address = address
        self.space = City(model_crs)

        self.roads = RoadNetwork(model_crs, address, simulation_radius)
        self.space.add_agents(mg.AgentCreator(Road, self).from_GeoDataFrame(self.roads.edges))

        self.buildings = Buildings(model_crs, address, simulation_radius)
        self.space.add_agents(mg.AgentCreator(Building, self).from_GeoDataFrame(self.buildings.df))

        self._create_population(population)

    def step(self) -> None:
        self.time += datetime.timedelta(minutes=5)
        self.agents.shuffle_do("step")

    def _create_population(self, population: dict[str, Any]) -> None:
        for p in population:
            person = Person(self, p['geometry'], self.crs, p['name'], p['age'], p['occupation'], p['plans'], p['current_activity'], p['current_location'], p['leave_time'])
            self.space.add_agents(person)

        