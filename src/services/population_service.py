from datetime import datetime
from src.services.llm_service import LLMService
from src.services.osm_service import OSMService

class PopulationService:
    llmService: LLMService
    osmService: OSMService

    def __init__(self):
        self.llmService = LLMService()
        self.osmService = OSMService()

    def generate_population(self, n_agents: int, address: str, date: datetime):
        agent_profiles = []
        feature_count = self.osmService.get_features_near_address(address)
        area_description = self.llmService.generate_area_description(address, feature_count)

        for _ in range(n_agents):
            new_profile = self.llmService.generate_person_profile(date, agent_profiles, address, feature_count, area_description)
            agent_profiles.append(new_profile)

        return agent_profiles
