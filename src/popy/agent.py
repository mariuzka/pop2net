"""Base class to create Agent objects."""

import agentpy as ap

from .location import Location

class Agent(ap.Agent):
    """This is a Base class to represent agents in the simulation.

    Agents' behavior can be implemented in classes that inherit from this.

    :param ap: _description_
    :type ap: _type_
    """

    def __init__(self, model, *args, **kwargs) -> None:
        """Agent Constructor.

        All parameters will be passed to the :class:`agentpy.Agent` parent.
        """
        super().__init__(model, *args, **kwargs)

        self.model = model
        self.model.env.add_agent(self)
        self.setup()

    def setup(self) -> None:
        """Instantiate an Agent.

        This is executed on the instantiation of each agent.
        """

    def neighbors(self) -> ap.AgentList:
        """Return all neighbors of an agent.

        Convenience method that returns all neighbors over all locations this agent is currently
        located in.

        Returns:
            :class:`agentpy.AgentList`: All agents co-located with this agent over all locations.
        """
        return self.model.env.neighbors_of_agent(self)

    def add_location(self, location: Location) -> None:
        """Add this Agent to a given location."""
        self.model.env.add_agent_to_location(self, location)

    @property
    def locations(self) -> ap.AgentList:
        """Return a list of locations that this agent is associated with.

        Returns:
            :class:`popy.LocationList`: A list of locations.
        """
        return self.model.env.locations_of_agent(self)

    def contact_weight(self, agent_v: "Agent") -> float:
        """Return the contact weight between this agent and a given other agent.

        This is summed over all shared locations.

        Returns:
            :float: A weight of the contact between the two agents.
        """
        contact_weight = 0
        for location in self.locations:
            if agent_v in location.agents:
                contact_weight += location.contact_weight(agent1=self, agent2=agent_v)
        return contact_weight
