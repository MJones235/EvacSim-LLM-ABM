

from datetime import datetime
from src.services.population_service import PopulationService
from mesa_geo.visualization import make_geospace_component
from mesa.visualization import SolaraViz
from mesa_geo.visualization import make_geospace_component
from src.simulation.model.model import EvacuationModel
from src.visualisation.solara_vis import agent_portrayal


address = "Loyalty Road, Hartlepool, UK"
n_agents = 5
simulation_start = datetime(2025, 2, 28, 11, 0, 0)
simulation_radius = 2000
crs = "epsg:27700"

population = PopulationService(crs).generate_population(n_agents, address, simulation_start)
model_params = {
    "address": address,
    "simulation_radius": simulation_radius,
    "population": population,
    "model_crs": crs
}
model = EvacuationModel(**model_params)
page = SolaraViz(
    model,
    [make_geospace_component(agent_portrayal)],
    name="EvacSim-LLM-ABM",
    model_params=model_params
)
page