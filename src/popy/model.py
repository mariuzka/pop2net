"""The model class. It encapsulates the full simulation."""
from __future__ import annotations

import agentpy as ap
import networkx as nx

import typing

from agentpy import AgentList
import networkx as nx

if typing.TYPE_CHECKING:
    from . import agent as _agent
    from . import location as _location

from popy.sequences import LocationList
import popy.utils as utils


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
        
        #TODO: evtl. verallgemeinern?
        for location in [location for location in self.locations if not location.static_weight]:
            location.update_weights()

        self.step()
        self.update()

        if self.t >= self._steps:  # type: ignore
            self.running = False
    

    @property
    def agents(self):
        return AgentList(
            model=self.model, 
            objs=[data["_obj"] for _, data in self.g.nodes(data=True) if data["bipartite"] == 0],
            )
    
    @property
    def locations(self):
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
        agent.env = self
        if not self.g.has_node(agent.id):
            self.g.add_node(agent.id, bipartite=0, _obj=agent)
    
    def add_agents(self, agents: list) -> None:
        for agent in agents:
            self.add_agent(agent)

    def add_location(self, location: _location.Location) -> None:
        """Add a location to the environment.

        The added location will have no connections to other agents or locatons by default.
        If the location is already in the current environment, this methods does nothing.

        Args:
            location: Location to be added to the environment.
        """
        location.env = self
        if not self.g.has_node(location.id):
            self.g.add_node(location.id, bipartite=1, _obj=location)
    
    def add_locations(self, locations: list) -> None:
        for location in locations:
            self.add_location(location)


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

    def remove_agents(self, agents: list) -> None:
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
        for location in locations:
            self.remove_location(location)
        
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

    def neighbors_of_agent(self, agent: _agent.Agent, location_classes: list = []) -> AgentList:
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
                and self.g.nodes[node]["_obj"].cls in location_classes
            )
        else:
            locations = (
                node 
                for node in self.g.neighbors(agent.id) 
                if self.g.nodes[node]["bipartite"] == 1
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
    
    #TODO: evlt. filtern nach Klasse oder Key einbauen
    def objects_between_objects(self, object1, object2):
        paths = list(
            nx.all_simple_paths(
                G=self.g, 
                source=object1.id, 
                target=object2.id, 
                cutoff=2,
                )
        )
        
        return [
            self.g.nodes[path[1]]["_obj"] for path in paths
            ]

    def locations_between_agents(self, agent1, agent2):
        return LocationList(
            model=self.model,
            objs=self.objects_between_objects(agent1, agent2)
        )
    
    def agents_between_locations(self, location1, location2):
        return AgentList(
            model=self.model,
            objs=self.objects_between_objects(location1, location2)
        )