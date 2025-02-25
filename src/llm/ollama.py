import ray
import json
from datetime import datetime
from ..osm.osm import OSM

@ray.remote
def call_ollama(prompt):
    from langchain_ollama import OllamaLLM
    return OllamaLLM(model="llama3.2:3b", temperature=0.9, top_p=0.95, top_k=50).invoke(prompt)     

class Ollama:
    _address: str
    _area_description: str

    def __init__(self, address: str):
        self._address = address
        self._area_description = self._get_area_description()

    def _get_area_description(self):
        formatted_summary = json.dumps(OSM().get_summary_of_area(self._address), indent=2)

        prompt = f"""
        Imagine you are writing a short, natural-language description of an area. 
        Using the following OpenStreetMap data as background information about the surroundings of {self._address}, generate a three-sentence description of the area. 
        Your final output should be one concise paragraph without any commentary or explanation. 
        
        OpenStreetMap data:
        {formatted_summary}
        """
        return ray.get(call_ollama.remote(prompt))


    def get_agent_profile(self, date: datetime, existing_profiles: list[object]):
        profiles_list = "\n".join(
            f"{profile['name']}, {profile['age']}, {profile['occupation']}"
            for profile in existing_profiles
        )
        prompt = f"""
        Imagine that it is {date.strftime("%-I.%M%p")} on {date.strftime("%A %-d %B")}, and you are observing a person at {self._address}.
        {self._area_description}

        These people are already known to be in the area:
        {profiles_list}

        Please generate a new, unique description of a person who might be present in this location at that time. 
        Return the description as a valid JSON object that includes exactly the following keys: 'name', 'age', and 'occupation'. 
        Each value should be realistic and reflect a plausible individual in this context, and must differ from the profiles provided above.
        Ensure that your response is the complete and only output.
        """
        text = ray.get(call_ollama.remote(prompt))
        return json.loads(text)

