import mesa_geo as mg
from datetime import datetime, timedelta

from src.simulation.decision.decision_module import DecisionModule

class Person(mg.GeoAgent):
    decision_module: DecisionModule

    name: str
    age: int
    occupation: str
    plans: list[str]
    current_activity: str
    current_location: str
    leave_time: datetime

    def __init__(self, model, geometry, crs, decision_module: DecisionModule, id: str, name: str, age: int, occupation: str, plans: list[str], current_activity: str, current_location: str, leave_time: datetime):
        super().__init__(model, geometry, crs)
        self.decision_module = decision_module

        self.unique_id = id
        self.name = name
        self.age = age
        self.occupation = occupation
        self.plans = plans
        self.current_activity = current_activity
        self.current_location = current_location
        self.leave_time = leave_time

    def step(self):
        if self.model.time >= self.leave_time:
            update = self.decision_module.decide_next_action(self)

            previous_location = self.current_location
            previous_activity = self.current_activity

            self.plans = update['updated_plans']
            self.current_activity = update['next_activity']
            self.current_location  = update['next_location']
            self.leave_time = self.model.time + timedelta(minutes=update['duration'])
            self.geometry = update['geometry']
            
            self.model.agent_decision_service.log_decision(
                run_id=self.model.run_id,
                agent_id=self.unique_id,
                previous_location=previous_location,
                previous_activity=previous_activity,
                next_location=self.current_location,
                next_activity=self.current_activity,
                reason=update["reason"],
                simulation_time=self.model.time
            )

