from src.services.osm_service import OSMService
from src.simulation.decision.decision_module import DecisionModule
from src.services.llm_service import LLMService
from src.simulation.agents.person import Person
from src.utils.location_utils import get_location_category, random_point_in_polygon

class GenerativeDecisionModule(DecisionModule):
    llm_service: LLMService
    osm_service: OSMService

    def __init__(self, llm_service: LLMService, osm_service: OSMService):
        self.llm_service = llm_service
        self.osm_service = osm_service

    def decide_next_action(self, agent: Person):
        update = self.llm_service.generate_next_destination(agent.model.run_id, agent, agent.model.time, agent.model.feature_count, agent.model.address)
        update['next_location'], category = get_location_category(agent.model.feature_count, update['next_location'])
        update['geometry'] = random_point_in_polygon(self.osm_service.get_feature_coordinates(agent.model.address, agent.model.simulation_radius, category, update['next_location'], agent.model.crs))
        return update