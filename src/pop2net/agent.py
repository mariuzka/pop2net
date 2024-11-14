"""Base class to create Agent objects."""

from __future__ import annotations

import typing
import warnings

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

    def neighbors(self, location_labels: list[str] | None = None) -> ap.AgentList:
        """Return all neighbors of an agent.

        Convenience method that returns all neighbors over all locations this agent is currently
        located in. The locations to be considered can be defined with location_labels.

        Args:
            location_labels: A list of location_labels.

        Returns:
            All agents co-located with this agent over all locations.
        """
        return self.model.neighbors_of_agent(self, location_labels=location_labels)

    def shared_locations(self, agent, location_labels: list[str] | None = None):
        return self.model.locations_between_agents(
            agent1=self,
            agent2=agent,
            location_labels=location_labels,
        )

    def add_location(self, location: _location.Location, weight: float | None = None) -> None:
        """Add this Agent to a given location.

        Args:
            location: Add agent to this location.
            weight (float | None): The edge weight between the agent and the location.
                Defaults to None.
        """
        self.model.add_agent_to_location(agent=self, location=location, weight=weight)

    def add_locations(self, locations: list, weight: float | None = None) -> None:
        """Add this agent to multiple locations.

        Args:
            locations (list): Add the agent to these locations.
            weight (float | None): The edge weight between the agent and the location.
                Defaults to None.
        """
        for location in locations:
            self.add_location(location=location, weight=weight)

    def remove_location(self, location: _location.Location) -> None:
        """Remove this Agent from a given location.

        Args:
            location: Remove agent from this location.
        """
        self.model.remove_agent_from_location(self, location)

    def remove_locations(self, locations: list) -> None:
        """Remove this Agent from the given locations.

        Args:
            locations (list): A list of location instances.
        """
        for location in locations:
            self.remove_location(location)

    @property
    def locations(self) -> _sequences.LocationList:
        """Return a list of locations that this agent is associated with.

        Returns:
            A list of locations.
        """
        return self.model.locations_of_agent(self)

    def get_agent_weight(self, agent: Agent, location_labels: list | None = None) -> float:
        """Return the edge weight between this agent and a given other agent.

        This is summed over all shared locations.

        Args:
            agent: The other agent.
            location_labels (list): A list of location classes to specify the type of locations
                which are considered.

        Returns:
            A weight of the contact between the two agents.
        """
        weight = 0
        for location in self.shared_locations(agent=agent, location_labels=location_labels):
            weight += location.project_weights(agent1=self, agent2=agent)
        return weight

    def get_location_weight(self, location) -> float:
        """Return the edge weight between this agent and a given location.

        Args:
            location (_type_): A location.

        Returns:
            float: The edge weight.
        """
        return self.model.get_weight(agent=self, location=location)

    def connect(self, agent: Agent, location_cls: type, weight: float | None = None):
        """Connects this agent with a given other agent via an instance of a given location class.

        Args:
            agent (list): An agent to connect with.
            location_cls (type): The location class that is used to create a location instance.
            weight(float | None): The edge weight between the agents and the location.
                Defaults to None.
        """
        self.model.connect_agents(agents=[self, agent], location_cls=location_cls, weight=weight)

    def disconnect(
        self,
        neighbor: Agent,
        location_labels: list | None = None,
        remove_self=True,
        remove_neighbor=True,
        remove_locations: bool = False,
    ):
        """Disconnects this agent from a given other agent by removing them from shared locations.

        If a list of location types is given, only shared locations of the given types are
        considered. Turn on `remove_locations` in order to not only remove the agents from the
        given location instance but also to remove the location instance from the model.  Keep in
        mind that this may affect other agents that are still connected with the location instance.

        Args:
            neighbor (Agent): An agent to disconnect from.
            location_labels (list | None, optional): A list of location types to specify which
            shared locations are considered. Defaults to None.
            remove_self (bool): Should the agent be removed from the shared locations?
                Defaults to True.
            remove_neighbor (bool): Should the neighbor be removed from the shared locations?
                Defaults to True.
            remove_locations (bool, optional): A bool that determines whether the shared locations
                shall be removed from the model. Defaults to False.
        """
        shared_locations = self.shared_locations(
            agent=neighbor,
            location_labels=location_labels,
        )

        for location in shared_locations:
            warn = False
            for agent in location.agents:
                if agent not in [self, neighbor]:
                    warn = True
                    break

            if remove_self:
                location.remove_agent(self)

                if warn:
                    msg = (
                        "There are other agents at the location from which you have removed agents."
                    )
                    warnings.warn(msg)

            if remove_neighbor:
                location.remove_agent(neighbor)

                if warn:
                    msg = (
                        "There are other agents at the location from which you have removed agents."
                    )
                    warnings.warn(msg)

            if remove_locations:
                self.model.remove_location(location)

                if warn:
                    msg = "You have removed a location to which other agents were still connected."
                    warnings.warn(msg)
