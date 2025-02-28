

from datetime import datetime
from src.repositories.model_outputs_repository import ModelOutputsRepository
from src.services.population_service import PopulationService
from src.simulation.model.model import EvacuationModel
import ray

class SimulationRunner:
    population_service: PopulationService
    model_outputs_repository: ModelOutputsRepository
    crs: str

    def __init__(self, crs: str):
        ray.init(ignore_reinit_error=True)
        self.crs = crs
        self.population_service = PopulationService(crs)
        self.model_outputs_repository = ModelOutputsRepository()

    def run(self, address:str, simulation_radius: float, n_agents: int, simulation_start: datetime):
        population = self.population_service.generate_population(n_agents, address, simulation_start)
        model_params = {
            "address": address,
            "simulation_radius": simulation_radius,
            "population": population,
            "start_time": simulation_start,
            "model_crs": self.crs
        }
        model = EvacuationModel(**model_params)
        model.run_model()
