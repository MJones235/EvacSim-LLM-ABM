from datetime import datetime, timedelta
from uuid import uuid4
from src.repositories.population_repository import PopulationRepository
from src.services.llm_service import LLMService
from src.services.osm_service import OSMService
from src.utils.location_utils import get_location_category, random_point_in_polygon
import random

class PopulationService:
    llm_service: LLMService
    osm_service: OSMService
    population_repository: PopulationRepository
    crs: str

    def __init__(self, crs: str):
        self.llm_service = LLMService()
        self.osm_service = OSMService()
        self.population_repository = PopulationRepository()
        self.crs = crs

    def generate_population(self, run_id: str, n_agents: int, address: str, radius_m: int, date: datetime) -> list[dict]:
        """
        Generates and stores a new population.
        """
        agent_profiles = []
        feature_count = self.osm_service.get_features_near_address(address, radius_m)
        area_description = self.llm_service.generate_area_description(run_id, address, feature_count)

        for _ in range(n_agents):
            sampled_profiles = random.sample(agent_profiles, min(10, len(agent_profiles)))
            new_profile = self.llm_service.generate_person_profile(run_id, date, sampled_profiles, address, feature_count, area_description)
            new_profile["id"] = str(uuid4())
            new_profile['current_location'], location_category = get_location_category(feature_count, new_profile['current_location'])
            new_profile['geometry'] = random_point_in_polygon(self.osm_service.get_feature_coordinates(address, radius_m, location_category, new_profile['current_location'], self.crs))
            new_profile['leave_time'] = date + timedelta(minutes=new_profile['duration'])
            agent_profiles.append(new_profile)

        # Save to database
        self.save_population(run_id, agent_profiles)
        return agent_profiles

    def get_population(self, run_id: str):
        """
        Retrieves population from a previous run.
        """
        return self.population_repository.get_population(run_id)
    
    def save_population(self, run_id: str, agent_profiles: list[dict], replace_id: bool = False):
        if replace_id:
            for profile in agent_profiles:
                profile["id"] = str(uuid4())
        self.population_repository.store_population(run_id, agent_profiles)
