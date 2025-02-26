from datetime import datetime
import click

from src.runners.simulation_runner import SimulationRunner

@click.group()
def cli():
    pass

@click.command()
@click.option("--address", default="Loyalty Road, Hartlepool, UK", help="Simulation location.")
@click.option("--radius", default=2000, type=int, help="Simulation radius in meters.")
@click.option("--n-agents", default=5, type=int, help="Number of agents in the simulation.")
@click.option("--start-time", type=click.DateTime(formats=["%Y-%m-%d %H:%M"]), 
              default=datetime.now().strftime("%Y-%m-%d %H:%M"),
              help="Simulation start time (format: YYYY-MM-DD HH:MM).")
@click.option("--visualise", is_flag=True, help="Run with Solara visualisation.")
def run_single(address, radius, n_agents, start_time, visualise):
    runner = SimulationRunner()
    runner.run(
        address=address,
        simulation_radius=radius,
        n_agents=n_agents,
        simulation_start=start_time,
        visualise=visualise
    )

    if not visualise:
        click.echo("Simulation completed. Results saved.")

cli.add_command(run_single)

if __name__ == "__main__":
    cli()
