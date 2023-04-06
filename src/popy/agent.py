import agentpy as ap

from .exceptions import PopyException
from .location import Location
from .sequences import LocationList


class Agent(ap.Agent):
    """This is a Base class to represent agents in the simulation.

    Agents' behavior can be implemented in classes that inherit from this.

    :param ap: _description_
    :type ap: _type_
    """

    def __init__(self, model, *args, **kwargs) -> None:
        super().__init__(model, *args, **kwargs)

        self.model = model
        self.model.env.add_agent(self)
        self.setup()

    def setup(self) -> None:
        """Setup function for the Agent.
        This is executed on the instantiation of each agent.
        """
        pass

    def neighbors(self, duplicates=False) -> ap.AgentList:
        """Convenience method that returns all neighbors over all locations this agent is currently
        located in.

        Returns:
            :class:`agentpy.AgentList`: All agents co-located with this agent over all locations.
        """
        return self.model.env.neighbors_of_agent(self)

    def add_location(self, location: Location) -> None:
        self.model.env.add_agent_to_location(self, location)

    @property
    def locations(self) -> ap.AgentList:
        return self.model.env.locations_of_agent(self)
