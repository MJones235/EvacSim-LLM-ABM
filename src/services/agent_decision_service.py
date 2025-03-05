from src.repositories.agent_decision_repository import AgentDecisionRepository
from datetime import datetime

class AgentDecisionService:
    def __init__(self):
        self.repository = AgentDecisionRepository()

    def log_decision(self, run_id: str, agent_id: int, previous_location: str, previous_activity: str, next_location: str, next_activity: str, reason: str, simulation_time: datetime):
        """Logs an agent's decision into the database."""
        timestamp = simulation_time.isoformat()
        self.repository.log_decision(run_id, agent_id, timestamp, previous_location, previous_activity, next_location, next_activity, reason)

    def get_agent_decisions(self, agent_id: int):
        """Retrieves all decisions made by a specific agent, ordered by timestamp."""
        return self.repository.get_decisions_by_agent(agent_id)