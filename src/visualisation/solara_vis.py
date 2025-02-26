import mesa_geo as mg

from src.simulation.agents.building import Building
from src.simulation.agents.geo_agents import Road

def agent_portrayal(agent: mg.GeoAgent) -> dict:
    portrayal = {}
    portrayal["color"] = "White"

    if isinstance(agent, Road):
        portrayal["color"] = "#D08004"
    elif isinstance(agent, Building):
        portrayal["color"] = "Grey"

    return portrayal
