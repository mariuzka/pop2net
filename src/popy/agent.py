import agentpy as ap

from .exceptions import PopyException
from .sequences import LocationList


class Agent(ap.Agent):
    """This is a Base class to represent agents in the simulation.

    Agents' behavior can be implemented in classes that inherit from this.

    :param ap: _description_
    :type ap: _type_
    """

    def __init__(self, model, *args, **kwargs):
        super().__init__(model, *args, **kwargs)

        self.model = model

    def get_contacts(self, duplicates=False):  # todo: new name = neighbors()
        neighbors = [
            neighbor for neighbors in self.locations.neighbors(self) for neighbor in neighbors
        ]
        neighbors = neighbors if duplicates else list(set(neighbors))
        return ap.AgentList(self.model, neighbors)

    @property
    def locations(self):
        return LocationList(
            self.model,
            [location for location in self.model.locations if location.is_affiliated(self)],
        )
