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
        self.locations = LocationList(model)

    def contacts(self, weights: bool = False):
        return ap.AgentList(
            self.model,
            [i for j in self.locations.neighbors(self) for i in j],
        )

    def add_location(self, location) -> None:
        """Assigns a location to this agent.

        Args:
            location (:doc:`location`):  Location that is to be added to the agent.

        Raises:
            PopyException: Raised, if the location is already assigned to this agent.
        """

        if location in self.locations:
            raise PopyException("Location already associated with this Agent!")
        self.locations.append(location)
        location.add_agent(self, visit_weight=1)

    def visit_locations(self, model) -> None:
        self.locations.visit(self)
