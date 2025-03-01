from datetime import datetime
from typing import Any
from src.simulation.agents.person import Person
from src.providers.llm_provider.llm_factory import LLMFactory
from src.providers.llm_provider.llm_provider import LLMProvider
from src.repositories.llm_logs_repository import LLMLogsRepository
import json
import hashlib

class LLMService:
    provider: LLMProvider
    llm_logs_repository: LLMLogsRepository

    def __init__(self, provider: str = "ollama"):
        self.provider = LLMFactory.get_provider(provider)
        self.llm_logs_repository = LLMLogsRepository()

    def query_llm(self, prompt: str, format: str = "json", use_cache: bool = False) -> dict | str:
        prompt_hash = self._hash_prompt(prompt)

        if use_cache:
            cached_response = self.llm_logs_repository.get_cached_response(prompt_hash)
            if cached_response:
                return json.loads(cached_response) if format == "json" else cached_response

        response = self.provider.call_llm(prompt, format)
        self.llm_logs_repository.cache_response(prompt_hash, prompt, json.dumps(response))

        return response
    
    def _hash_prompt(self, prompt: str) -> str:
        return hashlib.sha256(prompt.encode()).hexdigest()
    
    def generate_area_description(self, address: str, feature_count: dict[str, Any]):
        prompt = f"""
        Imagine you are writing a short, natural-language description of an area. 
        Using the following OpenStreetMap data as background information about the surroundings of {address}, generate a paragraph describing the area. 
        Your final output should be one paragraph without any commentary or explanation. 
        
        OpenStreetMap data giving a count of the features in the area:
        {json.dumps(feature_count, indent=2)}
        """
        return self.query_llm(prompt, format="", use_cache=True)

    
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
        Consider the time of day and day of the week.
        Return the description as a valid JSON object with:
        - 'name' (str)
        - 'age' (int)
        - 'occupation' (str)
        - 'current_location' (str, must be one of {list(feature_count["amenity"].keys()) + list(feature_count["building"].keys()) + list(feature_count["landuse"].keys())})
        - 'current_activity' (str, what is the agent currently doing)
        - 'duration' (int, how much longer will the person remain at their current location in minutes)
        - 'plans' (list of activities the person wants to carry out today)

        Ensure that your response is **only the JSON object**.
        """

        return self.query_llm(prompt, format="json", use_cache=False)
    
    def generate_next_destination(self, person: Person, date: datetime, feature_count: dict[str, Any], address:str):
        area_description = self.generate_area_description(address, feature_count)
        agent = person.__dict__
        prompt = f"""
        Imagine that it is {date.strftime("%R")} on {date.strftime("%A %e %B")}.
        You are simulating the movements of a person in {address}.
        {area_description}

        This is the current profile of the person:
        - Name: {agent["name"]}
        - Age: {agent["age"]}
        - Occupation: {agent["occupation"]}
        - Current Location: {agent["current_location"]}
        - Current Activity: {agent["current_activity"]}
        - Planned Activities: {', '.join(agent["plans"]) if agent["plans"] else "None"}

        Available locations nearby:
        - Amenities: {', '.join(feature_count["amenity"].keys())}
        - Buildings: {', '.join(feature_count["building"].keys())}
        - Land Use Areas: {', '.join(feature_count["landuse"].keys())}

        Please decide where the person will go next based on:
        - Their current activity and remaining time at their current location.
        - Their occupation, habits, and responsibilities.
        - The time of day and day of the week.
        - Their planned activities for the day.

        Return the decision as a JSON object with:
        - 'next_location' (str, must be one of the available locations above)
        - 'next_activity' (str, what the agent will do at the next location)
        - 'duration' (int, anticipated duration of the next activity in minutes)
        - 'updated_plans' (list of remaining activities after this action)

        Ensure that your response is **only the JSON object**.
        """

        return self.query_llm(prompt, format="json", use_cache=False)
