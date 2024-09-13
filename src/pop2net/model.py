"""The model class. It encapsulates the full simulation."""

from __future__ import annotations

import itertools
import typing
import warnings

import agentpy as ap
from agentpy import AgentList
import networkx as nx

if typing.TYPE_CHECKING:
    from . import agent as _agent
    from . import location as _location

from pop2net.sequences import LocationList
import pop2net.utils as utils


class Model(ap.Model):
    """Class the encapsulates a full simluation.

    This very closely follows the logic of the :class:`agentpy.Model` package. See
    :class:`agentpy.Model` for more information.
    """

    def __init__(self, parameters=None, _run_id=None, **kwargs):
        """Initiate a simulation.

        Args:
            parameters (dict, optional): An optional parameter dict that is passed to
            :class:`agentpy.Model`. Defaults to None.
            _run_id (int, optional): An optional _run_id that is passed to :class:`agentpy.Model`.
            Defaults to None.
            **kwargs: Optional parameters that are all passed to :class:`agentpy.Model`.
        """
        super().__init__(parameters, _run_id, **kwargs)
        self.g = nx.Graph()

    def sim_step(self) -> None:
        """Do 1 step in the simulation."""
        self.t += 1

        # TODO: Rethink the following:
        for location in self.locations:
            if hasattr(location, "static_weight") and hasattr(location, "_update_weights"):
                if not location.static_weight:
                    location._update_weights()

        self.step()
        self.update()

        if self.t >= self._steps:  # type: ignore
            self.running = False

    @property
    def agents(self) -> AgentList:
        """Show a iterable view of all agents in the environment.

        Returns:
            AgentList: A non-mutable AgentList of all agents in the environment.
        """
        return AgentList(
            model=self.model,
            objs=[data["_obj"] for _, data in self.g.nodes(data=True) if data["bipartite"] == 0],
        )

    @property
    def agents_by_id(self) -> dict:
        """Returns a dictionary which stores the model's agents by their id.

        Returns:
            dict: A dictionary which stores the model's agents by their id.
        """
        return {agent.id: agent for agent in self.agents}

    @property
    def locations_by_id(self) -> dict:
        """Returns a dictionary which stores the model's locations by their id.

        Returns:
            dict: A dictionary which stores the model's locations by their id.
        """
        return {location.id: location for location in self.locations}

    @property
    def locations(self) -> LocationList:
        """Show a iterable view of all locations in the environment.

        Returns:
            LocationList: a non-mutable LocationList of all locations in the environment.
        """
        return LocationList(
            model=self.model,
            objs=[data["_obj"] for _, data in self.g.nodes(data=True) if data["bipartite"] == 1],
        )

    def add_agent(self, agent: _agent.Agent) -> None:
        """Add an agent to the environment.

        The added agent will have no connections to other agents or locatons by default.
        If the agent is already in the current environment, this methods does nothing.

        Args:
            agent: Agent to be added to the environment.
        """
        if not self.g.has_node(agent.id):
            self.g.add_node(agent.id, bipartite=0, _obj=agent)

    def add_agents(self, agents: list) -> None:
        """Add agents to the environment.

        Args:
            agents (list): A list of the agents to be added.
        """
        for agent in agents:
            self.add_agent(agent)

    def add_location(self, location: _location.Location) -> None:
        """Add a location to the environment.

        The added location will have no connections to other agents or locatons by default.
        If the location is already in the current environment, this methods does nothing.

        Args:
            location: Location to be added to the environment.
        """
        if not self.g.has_node(location.id):
            self.g.add_node(location.id, bipartite=1, _obj=location)

    def add_locations(self, locations: list) -> None:
        """Add multiple locations to the environment at once.

        Args:
            locations (list): An iterable over multiple locations.
        """
        for location in locations:
            self.add_location(location)

    def add_agent_to_location(
        self,
        location: _location.Location,
        agent: _agent.Agent,
        weight: float = 1,
        **kwargs,
    ) -> None:
        """Add an agent to a specific location.

        Both the agent and the location have to be defined beforehand. All additional keyword
        arguments will be edge attributes for this connection.

        Args:
            location: Location the agent is to be added to.
            agent: Agent to be added to the location.
            weight: An optional weight for the connection.
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

        self.g.add_edge(agent.id, location.id, **kwargs)
        self.set_weight(agent=agent, location=location, weight=weight)

    def remove_agent(self, agent: _agent.Agent) -> None:
        """Remove an agent from the environment.

        If the agent does not exist in the environment, this method does nothing.

        Args:
            agent: Agent to be removed.
        """
        if self.g.has_node(agent.id):
            self.g.remove_node(agent.id)

    def remove_agents(self, agents: list) -> None:
        """Remove multiple agents from the environment at once.

        Args:
            agents (list): An iterable over multiple agents.
        """
        for agent in agents:
            self.remove_agent(agent)

    def remove_location(self, location: _location.Location) -> None:
        """Remove a location from the environment.

        If the location does not exist in the environment, this method does nothing.

        Args:
            location: Location to be removed.
        """
        if self.g.has_node(location.id):
            self.g.remove_node(location.id)

    def remove_locations(self, locations: list) -> None:
        """Remove multiple locations at once.

        Args:
            locations (list): An iterable over locations.
        """
        for location in locations:
            self.remove_location(location)

    def remove_agent_from_location(
        self,
        location: _location.Location,
        agent: _agent.Agent,
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

    def neighbors_of_agent(
        self,
        agent: _agent.Agent,
        location_classes: list | None = None,
    ) -> AgentList:
        """Return a list of neighboring agents for a specific agent.

        The locations to be considered can be defined with location_classes.

        Args:
            agent: Agent of whom the neighbors are to be returned.
            location_classes: A list of location_classes.

        Returns:
            The list of neighbors for the specified agent.
        """
        if location_classes:
            location_classes = [
                (utils._get_cls_as_str(cls) if not isinstance(cls, str) else cls)
                for cls in location_classes
            ]

            locations = (
                node
                for node in self.g.neighbors(agent.id)
                if self.g.nodes[node]["bipartite"] == 1
                and self.g.nodes[node]["_obj"].type in location_classes
            )
        else:
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

    # TODO: evlt. filtern nach Klasse oder Key einbauen
    def _objects_between_objects(self, object1, object2, object_classes: list | None = None):
        paths = list(
            nx.all_simple_paths(
                G=self.g,
                source=object1.id,
                target=object2.id,
                cutoff=2,
            ),
        )

        objects_between = [self.g.nodes[path[1]]["_obj"] for path in paths]

        if object_classes is not None:
            if len(object_classes) < 1:
                # TODO
                raise Exception

            object_classes = [
                (utils._get_cls_as_str(cls) if not isinstance(cls, str) else cls)
                for cls in object_classes
            ]
            filtered_objects_between = [o for o in objects_between if o.type in object_classes]
            return filtered_objects_between
        else:
            return objects_between

    def locations_between_agents(self, agent1, agent2, location_classes: list | None = None):
        """Return all locations the connect two agents.

        Args:
            agent1 (Agent): Agent 1.
            agent2 (Agent): Agent 2.
            location_classes (tuple, optional): Constrain the locations to the following types.
                Defaults to ().

        Returns:
            LocationList: A list of locations.
        """
        return LocationList(
            model=self.model,
            objs=self._objects_between_objects(agent1, agent2, location_classes),
        )

    def agents_between_locations(self, location1, location2, agent_classes: list | None = None):
        """Return all agents between two locations.

        Args:
            location1 (Location): Location 1.
            location2 (Location): Location 2.
            agent_classes (tuple, optional): Constrain the agents to the following types.
                Defaults to ().

        Returns:
            AgentList: A list of agents.
        """
        return AgentList(
            model=self.model,
            objs=self._objects_between_objects(location1, location2, agent_classes),
        )

    def set_weight(self, agent, location, weight) -> None:
        """Set the weight of an agent at a location.

        Args:
            agent (Agent): The agent.
            location (Location): The location.
            weight (int): The weight
        """
        self.g[agent.id][location.id]["weight"] = 1 if weight is None else weight

    def get_weight(self, agent, location) -> int:
        """Get the weight of an agent at a location.

        Args:
            agent (Agent): The agent.
            location (Location): The location.

        Returns:
            int: The weight.
        """
        return self.g[agent.id][location.id]["weight"]

    def connect_agents(self, agents: list, location_cls: type):
        """Connects multiple agents via an instance of a given location class.

        Args:
            agents (list): A list of agents.
            location_cls (type): The location class that is used to create a location instance.
        """
        location = location_cls(model=self)
        location.add_agents(agents)

    def disconnect_agents(
        self,
        agents: list,
        location_classes: list | None = None,
        remove_locations: bool = False,
    ):
        """Disconnects agents by removing them from shared locations.

        If a list of location types is given, only shared locations of the given types are
        considered. Turn on `remove_locations` in order to not only remove the given agents from the
        given location instance but also to remove the location instance from the model.
        Use this method with care because removing agents from locations also disconnects those
        agents from all other agents connected to the location. Removing the location instance from
        the model could have even more sideeffects to those agents still connected with this
        location!

        Args:
            agents (list): A list of agents.
            location_classes (list | None, optional): A list of location types to specify which
            shared locations are considered. Defaults to None.
            remove_locations (bool, optional): A bool that determines whether the shared locations
                shall be removed from the model. Defaults to False.
        """
        pairs = list(itertools.combinations(agents, 2))

        shared_locations = []

        for agent1, agent2 in pairs:
            shared_locations.extend(
                self.locations_between_agents(
                    agent1=agent1,
                    agent2=agent2,
                    location_classes=location_classes,
                )
            )

        shared_locations = set(shared_locations)

        for location in shared_locations:
            warn = False
            for agent in location.agents:
                if agent not in agents:
                    warn = True
                    break

            if warn:
                msg = "There are other agents at the location from which you have removed agents."
                warnings.warn(msg)

            location.remove_agents(agents)

            if remove_locations:
                self.remove_location(location=location)

                if warn:
                    msg = "You have removed a location to which other agents were still connected."
                    warnings.warn(msg)

    def export_bipartite_network(
        self,
        agent_attrs: list | None = None,
        location_attrs: list | None = None,
    ):
        graph = self.g.copy()

        for i in graph:
            if graph.nodes[i]["bipartite"] == 0:
                if agent_attrs is not None:
                    for agent_attr in agent_attrs:
                        graph.nodes[i][agent_attr] = getattr(graph.nodes[i]["_obj"], agent_attr)

            elif graph.nodes[i]["bipartite"] == 1:
                if location_attrs is not None:
                    for location_attr in location_attrs:
                        graph.nodes[i][location_attr] = getattr(
                            graph.nodes[i]["_obj"], location_attr
                        )

            del graph.nodes[i]["_obj"]
        return graph

    def export_agent_network(
        self,
        node_attrs: list | None = None,
        include_0_weights: bool = True,
    ) -> nx.Graph:
        """Creates a projection of the model's bipartite network.

        Args:
            node_attrs: A list of agent attributes
            include_0_weights: Should edges with weight 0 be displayed?

        Returns:
            A weighted graph created from a model's agent list. Agents are connected if they are
            neighbors in the model. Their connecting edge include the contact_weight as "weight"
            attribute.
        """
        graph = nx.Graph()

        # create nodes
        for agent in self.agents:
            if not graph.has_node(agent.id):
                node_attr_dict = (
                    {node_attr: vars(agent)[node_attr] for node_attr in node_attrs}
                    if node_attrs is not None
                    else {}
                )
                graph.add_node(agent.id, **node_attr_dict)

        # create edges
        for agent in self.agents:
            for agent_v in agent.neighbors():
                if not graph.has_edge(agent.id, agent_v.id):
                    weight = agent.get_agent_weight(agent_v)
                    if include_0_weights or weight > 0:
                        graph.add_edge(agent.id, agent_v.id, weight=weight)

        return graph
