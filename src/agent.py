import statistics as stats

import agentpy as ap

from .exceptions import PopyException
from .sequences import LocationList


class Agent(ap.Agent):
    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)

        self._model = model
        self.contact_diary = ap.AgentList(self._model)
        self.locations = LocationList(self._model)

    @property
    def contacts(self):
        return self.contact_diary.copy()

    def add_contact(self, agent) -> None:
        self.contact_diary.append(agent.id)

    def add_location(self, location) -> None:
        if location in self.locations:
            raise PopyException("Location already associated with this Agent!")
        self.locations.append(location)

    def clean_diary(self) -> None:
        self.contact_diary = ap.AgentList(self.model)

    def visit_locations(self, model) -> None:
        self.locations.visit(self)
