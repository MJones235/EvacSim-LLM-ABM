from shapely import Point
from src.repositories.repository import Repository
import json
from uuid import uuid4
from shapely.wkt import loads as wkt_loads
from datetime import datetime

class PopulationRepository(Repository):
    def table_name(self) -> str:
        return "population"

    def store_population(self, run_id: str, agent_profiles: list[dict]):
        """
        Stores a generated population in the database.
        """
        for agent in agent_profiles:
            data = {
                "run_id": run_id,
                "id": agent["id"],
                "name": agent["name"],
                "age": agent["age"],
                "occupation": agent["occupation"],
                "current_location": agent["current_location"],
                "current_activity": agent["current_activity"],
                "leave_time": agent["leave_time"].isoformat(),
                "plans": json.dumps(agent["plans"]),
                "geometry": agent["geometry"].wkt if isinstance(agent["geometry"], Point) else None
            }
            self.insert(data)

    def get_population(self, run_id: str) -> list[dict]:
        """
        Retrieves the population for a given run_id.
        """
        records = self.fetch_all("run_id = ?", (run_id,))
        return [
            {
                "id": record[0],
                "run_id": record[1],
                "name": record[2],
                "age": record[3],
                "occupation": record[4],
                "current_location": record[5],
                "current_activity": record[6],
                "leave_time": datetime.fromisoformat(record[7]),
                "plans": json.loads(record[8]),
                "geometry": wkt_loads(record[9]) if record[9] else None
            }
            for record in records
        ] if records else None
