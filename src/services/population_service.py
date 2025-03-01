from datetime import datetime, timedelta
from typing import Any
from src.services.llm_service import LLMService
from src.services.osm_service import OSMService
from src.utils.location_utils import get_location_category, random_point_in_polygon, weighted_random_selection

class PopulationService:
    llm_service: LLMService
    osm_service: OSMService
    crs: str

    def __init__(self, crs: str):
        self.llm_service = LLMService()
        self.osm_service = OSMService()
        self.crs = crs

    def generate_population(self, n_agents: int, address: str, radius_m: int, date: datetime):
        agent_profiles = []
        feature_count = self.osm_service.get_features_near_address(address, radius_m)
        area_description = self.llm_service.generate_area_description(address, feature_count)

        for _ in range(n_agents):
            new_profile = self.llm_service.generate_person_profile(date, agent_profiles, address, feature_count, area_description)
            
            new_profile['current_location'], location_category = get_location_category(feature_count, new_profile['current_location'])
            new_profile['geometry'] = random_point_in_polygon(self.osm_service.get_feature_coordinates(address, radius_m, location_category, new_profile['current_location'], self.crs))
            new_profile['leave_time'] = date + timedelta(minutes=new_profile['duration'])
            agent_profiles.append(new_profile)

        return agent_profiles
