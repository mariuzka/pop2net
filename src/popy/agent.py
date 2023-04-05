import agentpy as ap

from .exceptions import PopyException
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
        neighbors = [
                agent
                for neighbors in self.locations.neighbors(self)  # type: ignore
                for agent in neighbors
            ]
        neighbors = neighbors if duplicates else list(set(neighbors))
        return ap.AgentList(
            self.model,
            neighbors,
        )


    @property
    def locations(self):
        return LocationList(
            self.model,
            [location for location in self.model.locations if location.is_affiliated(self)],
        )
