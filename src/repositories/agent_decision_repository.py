from src.repositories.repository import Repository

class AgentDecisionRepository(Repository):
    
    def table_name(self) -> str:
        return "agent_decision_logs"

    def log_decision(self, run_id: str, agent_id: int, timestamp: str, previous_location: str, previous_activity: str, next_location: str, next_activity: str, reason: str):
        """Logs an agent's decision into the database."""
        data = {
            "run_id": run_id,
            "agent_id": agent_id,
            "timestamp": timestamp,
            "previous_location": previous_location,
            "previous_activity": previous_activity,
            "next_location": next_location,
            "next_activity": next_activity,
            "reason": reason
        }
        self.insert(data)

    def get_decisions_by_agent(self, agent_id: int):
        """Retrieves all decisions made by a specific agent, ordered by timestamp."""
        records = self.fetch_all("agent_id = ?", (agent_id,))
        return [
            {
                "id": record[0],
                "run_id": record[1],
                "agent_id": record[2],
                "timestamp": record[3],
                "previous_location": record[4],
                "previous_activity": record[5],
                "next_location": record[6],
                "next_activity": record[7],
                "reason": record[8]
            }
            for record in records
        ] if records else None