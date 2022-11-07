import agentpy as ap

from .exceptions import PopyException
from .sequences import LocationList


class Agent(ap.Agent):
    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)

        self.model = model
        self.locations = LocationList(model)

    def contacts(self, weights: bool = False):
        return ap.AgentList(
            self.model,
            [i for j in self.locations.neighbors(self) for i in j],
        )

    def add_location(self, location) -> None:
        if location in self.locations:
            raise PopyException("Location already associated with this Agent!")
        self.locations.append(location)
        location.add_agent(self, visit_weight=1)

    def visit_locations(self, model) -> None:
        self.locations.visit(self)
