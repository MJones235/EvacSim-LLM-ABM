import mesa_geo as mg

from ..agent.geo_agents import Road
from ..agent.building import Building

def agent_portrayal(agent: mg.GeoAgent) -> dict:
    portrayal = {}
    portrayal["color"] = "White"

    if isinstance(agent, Road):
        portrayal["color"] = "#D08004"
    elif isinstance(agent, Building):
        portrayal["color"] = "Grey"

    return portrayal
