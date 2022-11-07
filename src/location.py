from typing import Callable
from typing import Optional

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

    def add_agent(self, agent, visit_weight: int, visit_weight_mod: Optional[Callable] = None):
        if agent not in self.graph.agents:
            self.graph.add_agent(
                agent,
                visit_weight=visit_weight,
                visit_weight_mod=visit_weight_mod,
            )

    def remove_agent(self, agent):
        self.graph.remove_agent(agent)

    def edge_weight(self, agent1, agent2):
        return 1

    def neighbors(self, agent):
        return self.graph.neighbors(agent)

    def can_visit(self, agent):
        if self.model.is_weekday:
            return True
        return False

    def can_affiliate(self, agent):
        if agent.age < 18:
            return True

    def groupby(self):
        pass

    def visit(self, agent):
        if self.graph.g.nodes[agent.id]["visit_weight_mod"]:
            self.graph.g.nodes[agent.id]["visit_weight"] = self.graph.g.nodes[agent.id][
                "visit_weight_mod"
            ](self.graph.g.nodes[agent.id]["visit_weight"])

    # def connect_visitors(self, simultaneous=True):
    #     for u, v in self.graph.edges():
    #         visit_weight_u = self.graph.nodes[u]["visit_weight"]
    #         visit_weight_v = self.graph.nodes[v]["visit_weight"]

    #         if simultaneous:
    #             edge_weight = min((visit_weight_u, visit_weight_v)) / 24
    #         else:
    #             edge_weight = (visit_weight_u * visit_weight_v) / 576

    #         agent_u = self.graph.nodes[u]["visit_weight"]
    #         agent_u = self.graph.nodes[u]["_agent"]
