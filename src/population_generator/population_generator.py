from ..llm.ollama import Ollama
from datetime import datetime

class PopulationGenerator:
    def generate_population(self, n_agents: int, address: str, date: datetime):
        ollama = Ollama(address)
        agent_profiles = []
        for _ in range(n_agents):
            new_profile = ollama.get_agent_profile(date, agent_profiles)
            agent_profiles.append(new_profile)
        return agent_profiles