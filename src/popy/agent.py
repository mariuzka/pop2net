"""Base class to create Agent objects."""

from __future__ import annotations

import typing

import agentpy as ap

if typing.TYPE_CHECKING:
    from . import location as _location
    from . import sequences as _sequences


class Agent(ap.Agent):
    """This is a Base class to represent agents in the simulation.

    Agents' behavior can be implemented in classes that inherit from this.

    Examples:
        For instance, agents could all be instatiated with the `is_infected` attribute set to
        false::

            class InfectionAgent(Agent):
                def setup(self):
                    self.is_infected = False
    """

    def __init__(self, model, *args, **kwargs) -> None:
        """Agent Constructor.

        All parameters will be passed to the :class:`agentpy.Agent` parent.
        """
        super().__init__(model, *args, **kwargs)

        self.model = model

        self.model.add_agent(self)
        self.setup()

    def setup(self) -> None:
        """Instantiate an Agent.

        This is executed on the instantiation of each agent.
        """

    def neighbors(self, location_classes: list | None = None) -> ap.AgentList:
        """Return all neighbors of an agent.

        Convenience method that returns all neighbors over all locations this agent is currently
        located in. The locations to be considered can be defined with location_classes.

        Args:
            location_classes: A list of location_classes.

        Returns:
            All agents co-located with this agent over all locations.
        """
        return self.model.neighbors_of_agent(self, location_classes=location_classes)

    def shared_locations(self, agent, location_classes: list | None = None):
        return self.model.locations_between_agents(
            agent1=self,
            agent2=agent,
            location_classes=location_classes,
        )

    def add_location(self, location: _location.Location) -> None:
        """Add this Agent to a given location.

        Args:
            location: Add agent to this location.
        """
        self.model.add_agent_to_location(self, location)

    def add_locations(self, locations: list) -> None:
        for location in locations:
            self.add_location(location)

    def remove_location(self, location: _location.Location) -> None:
        """Remove this Agent from a given location.

        Args:
            location: Remove agent from this location.
        """
        self.model.remove_agent_from_location(self, location)

    def remove_locations(self, locations: list) -> None:
        for location in locations:
            self.remove_location(location)

    @property
    def locations(self) -> _sequences.LocationList:
        """Return a list of locations that this agent is associated with.

        Returns:
            A list of locations.
        """
        return self.model.locations_of_agent(self)

    def get_agent_weight(self, agent: Agent, location_classes: list | None = None) -> float:
        """Return the contact weight between this agent and a given other agent.

        This is summed over all shared locations.

        Args:
            agent_v: The other agent.

        Returns:
            A weight of the contact between the two agents.
        """
        weight = 0
        for location in self.shared_locations(agent=agent, location_classes=location_classes):
            weight += location.project_weights(agent1=self, agent2=agent)
        return weight

    def get_location_weight(self, location) -> float:
        return self.model.get_weight(agent=self, location=location)
