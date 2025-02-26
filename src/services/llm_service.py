from datetime import datetime
from typing import Any
from src.providers.llm_provider.llm_factory import LLMFactory
from src.providers.llm_provider.llm_provider import LLMProvider
from src.repositories.llm_logs_repository import LLMLogsRepository
import json

class LLMService:
    provider: LLMProvider
    llm_logs_repository: LLMLogsRepository

    def __init__(self, provider: str = "ollama"):
        self.provider = LLMFactory.get_provider(provider)
        self.llm_logs_repository = LLMLogsRepository()

    def query_llm(self, prompt: str, format: str = "json") -> dict | str:
        response = self.provider.call_llm(prompt, format)
        return response
    
    def generate_area_description(self, address: str, feature_count: dict[str, Any]):
        prompt = f"""
        Imagine you are writing a short, natural-language description of an area. 
        Using the following OpenStreetMap data as background information about the surroundings of {address}, generate a paragraph describing the area. 
        Your final output should be one paragraph without any commentary or explanation. 
        
        OpenStreetMap data giving a count of the features in the area:
        {json.dumps(feature_count, indent=2)}
        """
        return self.query_llm(prompt, format="")

    
    def generate_person_profile(self, date: datetime, existing_profiles: list[object], address: str, feature_count: dict[str, Any], area_description: str):
        profiles_list = "\n".join(
            f"{profile['name']}, {profile['age']}, {profile['occupation']}"
            for profile in existing_profiles
        ) if existing_profiles else "None"

        prompt = f"""
        Imagine that it is {date.strftime("%R")} on {date.strftime("%A %e %B")}, and you are observing a person at {address}.
        {area_description}

        These people are already known to be in the area:
        {profiles_list}

        Please generate a new, unique description of a person who might be present in this location at that time.
        Return the description as a valid JSON object with:
        - 'name' (str)
        - 'age' (int)
        - 'occupation' (str)
        - 'current_location' (str, must be one of {list(feature_count["amenity"].keys()) + list(feature_count["building"].keys()) + list(feature_count["landuse"].keys())})
        - 'leave_time' (ISO 8601 format)
        - 'plans' (list of activities)

        Ensure that your response is **only the JSON object**.
        """

        return self.query_llm(prompt, format="json")