from typing import Callable
from typing import Dict
from typing import Optional
from typing import Union

import agentpy as ap
import networkx as nx
from agentpy.sequences import AgentList


class FullGraph:
    def __init__(self, model) -> None:
        self.model = model
        self.g = nx.Graph()

    def add_agent(self, agent, **kwargs):

        self.g.add_node(agent.id, _agent=agent, **kwargs)
        for node in self.g.nodes():
            if node != agent.id:
                self.g.add_edge(agent.id, node)

    @property
    def agents(self):
        return AgentList(
            model=self.model,
            objs=[data["_agent"] for _u, data in self.g.nodes(data=True)],
        )

    def remove_agent(self, agent):
        self.g.remove_node(agent.id)

    def neighbors(self, agent, data: bool = False):

        temp = AgentList(self.model)
        for neighbor in self.g.neighbors(agent.id):
            temp.append(self.g.nodes[neighbor]["_agent"])

        return temp


class Location:
    def __init__(self, model, graph_cls=FullGraph) -> None:
        self.model = model
        self.graph = graph_cls(model=model)
        self.daily_visitors = ap.AgentList(model=self.model)
        self.n_current_visitors = 0
        self.subtype = None
        self.visit_weights: Dict[int, Union[int, float]] = {}

        # attributes that might be changed by customizing Location.setup()
        self.size: Optional[int] = None
        self.is_home = False

    def setup(self):
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
            self.n_current_visitors += 1

            if self not in agent.locations:
                agent.locations.append(self)

    # Should we do this?
    @property
    def agents(self):
        return self.graph.agents

    def remove_agent(self, agent):
        self.graph.remove_agent(agent)
        self.n_current_visitors -= 1

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

    def get_visit_weight(self, agent) -> Optional[Union[float, int]]:
        return None
