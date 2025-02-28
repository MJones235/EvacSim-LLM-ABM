import mesa_geo as mg
import solara
import pandas as pd

from src.simulation.model.model import EvacuationModel
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

@solara.component
def AgentProfileBrowser(model: EvacuationModel):
    agents = model.agents.select(agent_type=Person)

    if not agents:
        solara.Text("No agent profiles available.")
        return

    # Convert agents to DataFrame
    data = [
        {attr: getattr(agent, attr) for attr in ["name", "age", "occupation", "current_activity", "current_location", "leave_time", "plans"]}
        for agent in agents
    ]
    df = pd.DataFrame(data)
    df["plans"] = df["plans"].apply(lambda x: "; ".join(x) if isinstance(x, list) else str(x))
    solara.DataFrame(df, items_per_page=5)