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
        self.daily_visitors = ap.AgentList(model=self.model)
        self.subtype = None
        self.visit_weights: Dict[int, Union[int, float]] = {}

        # attributes that might be changed by customizing Location.setup()
        self.size: Optional[int] = None
        self.is_home = False

    def setup(self):
        pass

    def update(self):
        pass

    def add_agent(
        self,
        agent,
        visit_weight: Optional[int] = None,
        visit_weight_mod: Optional[Callable] = None,
    ):
        if not self.can_affiliate(agent):
            return
        if agent not in self.graph.agents:
            self.graph.add_agent(
                agent,
                visit_weight=visit_weight,
                visit_weight_mod=visit_weight_mod,
            )

            if self not in agent.locations:
                agent.locations.append(self)

    @property
    def agents(self):
        return self.graph.agents

    @property
    def n_current_visitors(self):
        return self.graph.g.number_of_nodes() - 1

    def remove_agent(self, agent):
        self.graph.remove_agent(agent)

    def edge_weight(self, agent1, agent2):
        return 1

    def neighbors(self, agent):
        return self.graph.neighbors(agent)

    def can_visit(self, agent) -> bool:
        return True

    def can_affiliate(self, agent) -> bool:
        return True

    def groupby(self, agent):
        return None

    def get_visit_weight(self, agent) -> float:
        return 1
