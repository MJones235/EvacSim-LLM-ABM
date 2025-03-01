import mesa_geo as mg
from datetime import datetime
import uuid

class Person(mg.GeoAgent):
    name: str
    age: int
    occupation: str
    plans: list[str]
    current_activity: str
    current_location: str
    leave_time: datetime

    def __init__(self, model, geometry, crs, name: str, age: int, occupation: str, plans: list[str], current_activity: str, current_location: str, leave_time: datetime):
        super().__init__(model, geometry, crs)

        self.unique_id = uuid.uuid4().int
        self.name = name
        self.age = age
        self.occupation = occupation
        self.plans = plans
        self.current_activity = current_activity
        self.current_location = current_location
        self.leave_time = leave_time

    def step(self):
        if self.model.time >= self.leave_time:
            feature_count = self.model.osm_service.get_features_near_address(self.model.address)
            update = self.model.llm_service.generate_next_destination(self, self.model.time, feature_count, self.model.address)
            print(update)