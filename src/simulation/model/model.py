from typing import Any
import mesa
import mesa_geo as mg
import datetime

from src.simulation.decision.generative_decision_module import GenerativeDecisionModule
from src.services.population_service import PopulationService
from src.services.llm_service import LLMService
from src.services.osm_service import OSMService
from src.services.agent_decision_service import AgentDecisionService

from ..agents.person import Person

from ..environment.road_network import RoadNetwork
from ..environment.city import City
from ..environment.buildings import Buildings
from ..agents.road import Road
from ..agents.building import Building

class EvacuationModel(mesa.Model):
    run_id: str

    roads: RoadNetwork
    space: City
    buildings: Buildings
    crs: str
    time: datetime
    address: str
    simulation_radius: int
    feature_count: dict[str, Any]

    llm_service: LLMService
    osm_service: OSMService
    population_service: PopulationService
    agent_decision_service: AgentDecisionService

    def __init__(
        self, 
        run_id: str,
        address: str,
        simulation_radius: float,
        population: dict[str, Any],
        start_time: datetime,
        model_crs: str,
        n_agents: int
    ) -> None:
        super().__init__()
        self.run_id = run_id

        self.llm_service = LLMService()
        self.osm_service = OSMService()
        self.population_service = PopulationService(model_crs)
        self.agent_decision_service = AgentDecisionService()

        self.crs = model_crs
        self.time = start_time
        self.address = address
        self.simulation_radius = simulation_radius
        self.feature_count = self.osm_service.get_features_near_address(self.address, self.simulation_radius)

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
        decision_module = GenerativeDecisionModule(self.llm_service, self.osm_service)
        for p in population:
            person = Person(self, p['geometry'], self.crs, decision_module, p['id'], p['name'], p['age'], p['occupation'], p['plans'], p['current_activity'], p['current_location'], p['leave_time'])
            self.space.add_agents(person)

        