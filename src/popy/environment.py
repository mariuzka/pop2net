"""A simulation environment.

This class is the basis for all interactions during the simulation.
"""
from __future__ import annotations

import typing

from agentpy import AgentList
import networkx as nx

if typing.TYPE_CHECKING:
    from . import agent as _agent
    from . import location as _location
    from . import model as _model

from popy.sequences import LocationList

class Environment:
    """The simulation environment."""

    def __init__(self, model: _model.Model) -> None:
        """Instantiate the environment and add it to its model.

        Args:
            model: Model this environment should be associated with.
        """
        self.model = model
        self.g = nx.Graph()

    def add_agent(self, agent: _agent.Agent) -> None:
        """Add an agent to the environment.

        The added agent will have no connections to other agents or locatons by default.
        If the agent is already in the current environment, this methods does nothing.

        Args:
            agent: Agent to be added to the environment.
        """
        if not self.g.has_node(agent.id):
            self.g.add_node(agent.id, bipartite=0, _obj=agent)

    def add_location(self, location: _location.Location) -> None:
        """Add a location to the environment.

        The added location will have no connections to other agents or locatons by default.
        If the location is already in the current environment, this methods does nothing.

        Args:
            location: Location to be added to the environment.
        """
        if not self.g.has_node(location.id):
            self.g.add_node(location.id, bipartite=1, _obj=location)

    def add_agent_to_location(
        self, location: _location.Location, agent: _agent.Agent, **kwargs,
    ) -> None:
        """Add an agent to a specific location.

        Both the agent and the location have to be defined beforehand. All additional keyword
        arguments will be edge attributes for this connection.

        Args:
            location: Location the agent is to be added to.
            agent: Agent to be added to the location.
            **kwargs: Additional edge attributes.

        Raises:
            Exception: Raised if the location does not exist in the environment.
            Exception: Raised if the agent does not exist in the environment.
        """
        # TODO: Create custom exceptions
        if not self.g.has_node(location.id):
            msg = f"Location {location} does not exist in Environment!"
            raise Exception(msg)
        if not self.g.has_node(agent.id):
            msg = f"Agent {agent} does not exist in Environment!"
            raise Exception(msg)

        if not self.g.has_edge(agent.id, location.id):
            self.g.add_edge(agent.id, location.id, **kwargs)

    def remove_agent(self, agent: _agent.Agent) -> None:
        """Remove an agent from the environment.

        If the agent does not exist in the environment, this method does nothing.

        Args:
            agent: Agent to be removed.
        """
        if self.g.has_node(agent.id):
            self.g.remove_node(agent.id)

    def remove_location(self, location: _location.Location) -> None:
        """Remove a location from the environment.

        If the location does not exist in the environment, this method does nothing.

        Args:
            location: Location to be removed.
        """
        if self.g.has_node(location.id):
            self.g.remove_node(location.id)

    def remove_agent_from_location(
        self, location: _location.Location, agent: _agent.Agent,
    ) -> None:
        """Remove an agent from a location.

        Args:
            location: Location, the agent is to be removed from.
            agent: Agent to be disassociated with the location.

        Raises:
            Exception: Raised if the location does not exist in the environment.
            Exception: Raised if the agent does not exist in the environment.
        """
        # TODO: use custom exceptions
        if not self.g.has_node(location.id):
            msg = f"Location {location} does not exist in Environment!"
            raise Exception(msg)
        if not self.g.has_node(agent.id):
            msg = f"Agent {agent} does not exist in Environment!"
            raise Exception(msg)

        if self.g.has_edge(agent.id, location.id):
            self.g.remove_edge(agent.id, location.id)

    def agents_of_location(self, location: _location.Location) -> AgentList:
        """Return the list of agents associated with a specific location.

        Args:
            location: The desired location.

        Returns:
            A list of agents.
        """
        nodes = self.g.neighbors(location.id)
        return AgentList(
            self.model,
            (self.g.nodes[node]["_obj"] for node in nodes if self.g.nodes[node]["bipartite"] == 0),
        )

    def locations_of_agent(self, agent: _agent.Agent) -> LocationList:
        """Return the list of locations associated with a specific agent.

        Args:
            agent: The desired agent.

        Returns:
            A list of locations.
        """
        nodes = self.g.neighbors(agent.id)
        return LocationList(
            self.model,
            (self.g.nodes[node]["_obj"] for node in nodes if self.g.nodes[node]["bipartite"] == 1),
        )

    def neighbors_of_agent(self, agent: _agent.Agent) -> AgentList:
        """Return a list of neighboring agents for a specific agent.

        Args:
            agent: Agent of whom the neighbors are to be returned.

        Returns:
            The list of neighbors for the specified agent.
        """
        locations = (
            node for node in self.g.neighbors(agent.id) if self.g.nodes[node]["bipartite"] == 1
        )
        neighbor_agents = {
            agent_id
            for location_id in locations
            for agent_id in self.g.neighbors(location_id)
            if self.g.nodes[agent_id]["bipartite"] == 0
        }
        return AgentList(
            self.model,
            (
                self.g.nodes[agent_id]["_obj"]
                for agent_id in neighbor_agents
                if agent_id != agent.id
            ),
        )

    def set_edge_attribute(
        self, location: _location.Location, agent: _agent.Agent, attr_name: str, attr_value,
    ) -> None:
        """Set a specific edge attribute for the connection between an agent and a location.

        Args:
            location: Location for the edge.
            agent: Agent for the edge.
            attr_name: Name of the edge attribute.
            attr_value: Value of the edge attribute.
        """
        self.g[agent.id][location.id][attr_name] = attr_value
