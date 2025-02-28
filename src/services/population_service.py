from datetime import datetime, timedelta
from typing import Any
from src.services.llm_service import LLMService
from src.services.osm_service import OSMService
from src.utils.location_utils import get_location_category, random_point_in_polygon, weighted_random_selection

class PopulationService:
    llmService: LLMService
    osmService: OSMService
    crs: str

    def __init__(self, crs: str):
        self.llmService = LLMService()
        self.osmService = OSMService()
        self.crs = crs

    def generate_population(self, n_agents: int, address: str, date: datetime):
        agent_profiles = []
        search_radius_m = 500
        feature_count = self.osmService.get_features_near_address(address, search_radius_m)
        area_description = self.llmService.generate_area_description(address, feature_count)

        for _ in range(n_agents):
            new_profile = self.llmService.generate_person_profile(date, agent_profiles, address, feature_count, area_description)
            try:
                location_category = get_location_category(feature_count, new_profile['current_location'])
                new_profile['geometry'] = random_point_in_polygon(self.osmService.get_feature_coordinates(address, search_radius_m, location_category, new_profile['current_location'], self.crs))
            except ValueError:
                (category, location) = weighted_random_selection(feature_count)
                new_profile['geometry'] = random_point_in_polygon(self.osmService.get_feature_coordinates(address, search_radius_m, category, location, self.crs))
            new_profile['leave_time'] = date + timedelta(minutes=new_profile['duration'])
            agent_profiles.append(new_profile)

        return agent_profiles