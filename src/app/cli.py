from datetime import datetime
import sys
from mesa.visualization import SolaraViz
from mesa_geo.visualization import make_geospace_component
from src.visualisation.solara_vis import AgentProfileBrowser, Clock, agent_portrayal
from src.runners.simulation_runner import SimulationRunner

def parse_args():
    args = {
        "address": "Loyalty Road, Hartlepool, UK",
        "radius": 2000,
        "n_agents": 5,
        "start_time": datetime.now(),
        "crs": "epsg:27700",
        "interactive": False
    }

    expected_args = {
        "--address": str,
        "--radius": int,
        "--n-agents": int,
        "--start-time": str,
        "--crs": str
    }

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]

        if arg in expected_args and i + 1 < len(sys.argv):
            arg_type = expected_args[arg]
            try:
                value = sys.argv[i + 1]
                if arg == "--start-time":
                    try:
                        args["start_time"] = datetime.strptime(value, "%Y-%m-%d %H:%M")
                    except ValueError:
                        print(f"Invalid start time format '{value}'. Expected 'YYYY-MM-DD HH:MM'. Using default.")
                else:
                    args[arg.lstrip("--").replace("-", "_")] = arg_type(value)
                i += 1  
            except ValueError:
                print(f"Invalid value for {arg}. Expected {arg_type.__name__}, got '{sys.argv[i + 1]}'. Using default.")
        
        elif arg == "--interactive":
            args["interactive"] = True
        
        i += 1

    return args


if __name__ == "__main__":
    args = parse_args()
    runner = SimulationRunner(args["crs"])
    model, params = runner.get_model(args["address"], args["radius"], args["n_agents"], args["start_time"])
    if args["interactive"]:
        page = SolaraViz(
        model,
        [
            make_geospace_component(agent_portrayal),
            AgentProfileBrowser,
            Clock
        ],
        name="EvacSim-LLM-ABM",
        model_params=params
        )
        page
    
    else:
        model.run_model()

