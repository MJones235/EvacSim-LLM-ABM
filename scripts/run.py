from src.model.model import EvacuationModel
from src.visualisation.utils import agent_portrayal
from src.population_generator.population_generator import PopulationGenerator
from mesa.visualization import SolaraViz
from mesa_geo.visualization import make_geospace_component
from datetime import datetime
import ray

ray.init(ignore_reinit_error=True)

address = "Loyalty Road, Hartlepool, TS25 5BA, UK"
date = datetime(2025, 2, 25, 9, 30)
n_agents = 10
population = PopulationGenerator().generate_population(n_agents, address, date)
print(population)

model_params = {
    "address": address,
    "simulation_radius": 2000
}
model = EvacuationModel(**model_params)
page = SolaraViz(
    model,
    [make_geospace_component(agent_portrayal)],
    name="EvacSim-LLM-ABM",
    model_params=model_params
)
page
