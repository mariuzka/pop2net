from typing import Callable
from typing import Dict
from typing import Optional
from typing import Union

import agentpy as ap
import networkx as nx
from agentpy.objects import Object
from agentpy.sequences import AgentList


class FullGraph:
    def __init__(self, location_id, model) -> None:
        self.location_id = location_id
        self.model = model
        self.g = nx.Graph()
        self.g.add_node(f"L{location_id}", bipartite=1)

    def add_agent(self, agent, **kwargs):
        self.g.add_node(agent.id, _agent=agent, bipartite=0, **kwargs)
        self.g.add_edge(agent.id, f"L{self.location_id}")

    @property
    def agents(self):
        return AgentList(
            model=self.model,
            objs=[
                data["_agent"] for _u, data in self.g.nodes(data=True) if data["bipartite"] == 0
            ],
        )

    def remove_agent(self, agent):
        self.g.remove_node(agent.id)

    def neighbors(self, agent) -> AgentList:
        agents = AgentList(self.model)
        for neighbor, data in self.g.nodes(data=True):
            if neighbor != agent.id and data["bipartite"] == 0:
                agents.append(data["_agent"])

        return agents


class Location(Object):
    def __init__(self, model, graph_cls=FullGraph) -> None:
        super().__init__(model)
        self.model = model
        self.graph = graph_cls(self.id, model)
        self.subtype = None
        self.size: Optional[int] = None

    def setup(self):
        """
        ~ User interface ~
        """
        pass

    def _add_agent(
        self,
        agent,
    ):
        if not self.can_affiliate(agent):
            return
        if agent not in self.graph.agents:
            self.graph.add_agent(agent)

    def add_agent(self, agent):  # todo: new name = add()
        self._add_agent(agent)

    @property
    def agents(self):
        return self.graph.agents

    @property
    def n_current_visitors(self):
        return self.graph.g.number_of_nodes() - 1

    def _remove_agent(self, agent):  # todo: new name = remove()
        self.graph.remove_agent(agent)

    def remove_agent(self, agent):
        self._remove_agent(agent)

    def neighbors(self, agent):
        return self.graph.neighbors(agent)

    def can_affiliate(self, agent) -> bool:  # todo: new name = join()
        """
        ~ User interface ~
        """
        return True

    def groupby(self, agent):  # todo: new name = group()
        """
        ~ User interface ~
        """
        return None

    def is_affiliated(self, agent) -> bool:
        return agent in self.graph.agents


class WeightedLocation(Location):
    def __init__(self, model, graph_cls=FullGraph) -> None:
        super().__init__(model, graph_cls)
        self.weights: Dict[int, float] = {}

    def weight(self, agent) -> float:
        """
        ~ User interface ~

        Defines how the edge weight between an agent and the location is determined.
        """
        return 1

    def update_weight(self, agent) -> None:
        """
        Creates or updates the agent-speific weight in the location-specific dictionary of weights.
        """
        self.weights[agent.id] = self.weight(agent)

    def update_weights(self) -> None:
        """
        Update the weight of every agent on this location.
        """
        for agent in self.agents:
            self.update_weight(agent)

    def add_agent(self, agent) -> None:
        """
        Adds an agent to the graph and the corresponding weight to the dictionary of weights.
        """
        self._add_agent(agent)
        self.update_weight(agent)

    def remove_agent(self, agent) -> None:
        """
        Removes the agent from the graph and the weight from the dictionary of weights.
        """
        self._remove_agent(agent)
        del self.weights[agent.id]

    def get_weight(self, agent) -> float:
        """
        Returns the edge weight between an agent and the location.
        """
        return self.weights[agent.id]

    def edge_weight(
        self,
        agent1,
        agent2,
        method: str = "average",
        denominator: float = 1,
    ) -> float:
        """
        ~ User interface ~

        Defines how the weights are combined when the edge weight between two agent is determined.
        Can be completely rewritten to have location-specific methods of this kind with the same name or can be used as it is in the simulation code.
        """

        if method == "average":
            return self.edge_weight_random(agent1, agent2, denominator)

        elif method == "simultan":
            return self.edge_weight_simultan(agent1, agent2, denominator)
        else:
            raise Exception(f"There is no method to combine the weights which is called {method}.")

    def edge_weight_average(self, agent1, agent2, denominator: float = 1) -> float:
        """
        Determines the average amount of time the two agents are at the location simultaneously.
        """
        return (self.get_weight(agent1) * self.get_weight(agent2)) / (denominator * denominator)

    def edge_weight_simultan(self, agent1, agent2, denominator: float = 1) -> float:
        """
        Determines the maximum amount of time which the two agents could be at this location at the same time.
        """
        return min(self.get_weight(agent1), self.get_weight(agent2)) / denominator
