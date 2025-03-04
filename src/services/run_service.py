from datetime import datetime
from uuid import uuid4
from src.repositories.run_repository import RunRepository

class RunService:
    def __init__(self):
        self.run_repository = RunRepository()

    def create_run(self, address: str, simulation_radius: float, n_agents: int, simulation_time: datetime) -> str:
        """
        Creates a new simulation run entry in the database.

        :param address: The address where the simulation starts.
        :param simulation_radius: The radius of the simulation in meters.
        :param n_agents: Number of agents in the simulation.
        :param simulation_time: The start time of the simulation.
        :return: The generated run ID.
        """
        run_id = str(uuid4())  # Generate a unique run ID

        metadata = {
            "run_id": run_id,
            "address": address,
            "simulation_radius": simulation_radius,
            "n_agents": n_agents,
            "simulation_time": simulation_time
        }

        self.run_repository.store_run_metadata(metadata)
        return run_id

    def get_run(self, run_id: str):
        """
        Retrieves a specific run's metadata.

        :param run_id: The unique ID of the simulation run.
        :return: A dictionary containing the run metadata or None if not found.
        """
        return self.run_repository.fetch_run_metadata(run_id)

    def list_runs(self):
        """
        Retrieves a list of all simulation runs.

        :return: A list of dictionaries containing metadata of all runs.
        """
        return self.run_repository.fetch_all_runs()

    def delete_run(self, run_id: str):
        """
        Deletes a simulation run by ID.

        :param run_id: The unique ID of the simulation run to delete.
        """
        self.run_repository.delete_run(run_id)
