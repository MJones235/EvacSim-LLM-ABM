

from datetime import datetime
from src.services.run_service import RunService
from src.repositories.model_outputs_repository import ModelOutputsRepository
from src.services.population_service import PopulationService
from src.simulation.model.model import EvacuationModel
import ray

class SimulationRunner:
    population_service: PopulationService
    model_outputs_repository: ModelOutputsRepository
    run_service: RunService
    crs: str

    def __init__(self, crs: str):
        ray.init(ignore_reinit_error=True)
        self.crs = crs
        self.population_service = PopulationService(crs)
        self.model_outputs_repository = ModelOutputsRepository()
        self.run_service = RunService()

    def get_model(self, address: str = None, simulation_radius: float = None, 
                  n_agents: int = None, simulation_start: datetime = None, 
                  previous_run_id: str = None):
        """
        Retrieves or generates a simulation model.
        - If `previous_run_id` is provided, all parameters are copied from that run.
        - Otherwise, a new simulation is created with provided parameters.
        """
        if previous_run_id:
            # Retrieve parameters from previous run
            previous_params = self.run_service.get_run(previous_run_id)
            if not previous_params:
                raise ValueError(f"Run ID {previous_run_id} not found.")

            # Copy parameters
            run_id = self.run_service.create_run(
                previous_params[3],
                previous_params[4],
                previous_params[5],
                datetime.fromisoformat(previous_params[2])
            )

            # Retrieve population from the previous run
            population = self.population_service.get_population(previous_run_id)

        else:
            # Ensure required parameters are provided
            if not all([address, simulation_radius, n_agents, simulation_start]):
                raise ValueError("Must provide simulation parameters if not using a previous run.")

            run_id = self.run_service.create_run(address, simulation_radius, n_agents, simulation_start)

            # Generate a new population
            population = self.population_service.generate_population(run_id, n_agents, address, simulation_radius, simulation_start)

        # Create model with parameters
        model_params = {
            "run_id": run_id,
            "address": address or previous_params[3],
            "simulation_radius": simulation_radius or previous_params[4],
            "n_agents": n_agents or previous_params[5],
            "start_time": simulation_start or datetime.fromisoformat(previous_params[2]),
            "model_crs": self.crs,
            "population": population
        }

        model = EvacuationModel(**model_params)
        return model, model_params