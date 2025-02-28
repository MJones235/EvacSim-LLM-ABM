import mesa_geo as mg

from src.simulation.agents.person import Person
from src.simulation.agents.building import Building
from src.simulation.agents.geo_agents import Road

def agent_portrayal(agent: mg.GeoAgent) -> dict:
    portrayal = {}
    portrayal["color"] = "White"

    if isinstance(agent, Road):
        portrayal["color"] = "Orange"
    elif isinstance(agent, Building):
        portrayal["color"] = "Grey"
    elif isinstance(agent, Person):
        portrayal["color"] = "Green"
        
    return portrayal
