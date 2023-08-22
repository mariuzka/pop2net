from agentpy import AgentList
import networkx as nx

from popy import Agent
from popy import Location
from popy.sequences import LocationList

class Environment:
    def __init__(self, model) -> None:
        self.model = model
        self.g = nx.Graph()

    def add_agent(self, agent: Agent) -> None:
        if not self.g.has_node(agent.id):
            self.g.add_node(agent.id, bipartite=0, _obj=agent)

    def add_location(self, location: Location) -> None:
        if not self.g.has_node(location.id):
            self.g.add_node(location.id, bipartite=1, _obj=location)

    def add_agent_to_location(self, location, agent, **kwargs) -> None:
        if not self.g.has_node(location.id):
            raise Exception("Location {} does not exist in Environment!".format(location))
        if not self.g.has_node(agent.id):
            raise Exception("Agent {} does not exist in Environment!".format(agent))

        if not self.g.has_edge(agent.id, location.id):
            self.g.add_edge(agent.id, location.id, **kwargs)

    def remove_agent(self, agent: Agent) -> None:
        if self.g.has_node(agent.id):
            self.g.remove_node(agent.id)

    def remove_location(self, location: Location) -> None:
        if self.g.has_node(location.id):
            self.g.remove_node(location.id)

    def remove_agent_from_location(self, location, agent) -> None:
        if not self.g.has_node(location.id):
            raise Exception("Location {} does not exist in Environment!".format(location))
        if not self.g.has_node(agent.id):
            raise Exception("Agent {} does not exist in Environment!".format(agent))

        if self.g.has_edge(agent.id, location.id):
            self.g.remove_edge(agent.id, location.id)

    def agents_of_location(self, location: Location) -> AgentList:
        nodes = self.g.neighbors(location.id)
        return AgentList(
            self.model,
            (self.g.nodes[node]["_obj"] for node in nodes if self.g.nodes[node]["bipartite"] == 0),
        )

    def locations_of_agent(self, agent: Agent) -> LocationList:
        nodes = self.g.neighbors(agent.id)
        return LocationList(
            self.model,
            (self.g.nodes[node]["_obj"] for node in nodes if self.g.nodes[node]["bipartite"] == 1),
        )

    def neighbors_of_agent(self, agent: Agent):
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

    def set_edge_attribute(self, location, agent, attr_name: str, attr_value):
        self.g[agent.id][location.id][attr_name] = attr_value
