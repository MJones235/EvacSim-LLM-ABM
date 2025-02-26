

from datetime import datetime
from src.repositories.model_outputs_repository import ModelOutputsRepository
from src.services.population_service import PopulationService
from src.simulation.model.model import EvacuationModel
from mesa.visualization import SolaraViz
from mesa_geo.visualization import make_geospace_component
import ray

from src.visualisation.solara_vis import agent_portrayal

class SimulationRunner:
    population_service: PopulationService
    model_outputs_repository: ModelOutputsRepository

    def __init__(self):
        ray.init(ignore_reinit_error=True)
        self.population_service = PopulationService()
        self.model_outputs_repository = ModelOutputsRepository()

    def run(self, address:str, simulation_radius: float, n_agents: int, simulation_start: datetime, visualise=False):
        population = self.population_service.generate_population(n_agents, address, simulation_start)
        model_params = {
            "address": address,
            "simulation_radius": simulation_radius
        }
        model = EvacuationModel(**model_params)
        if (visualise):
            page = SolaraViz(
                model,
                [make_geospace_component(agent_portrayal)],
                name="EvacSim-LLM-ABM",
                model_params=model_params
            )
            page
        else:
            model.run_model()
