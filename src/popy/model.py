import agentpy as ap
import networkx as nx
from networkx import bipartite

from popy.environment import Environment

class Model(ap.Model):
    """Class the encapsulates a full simluation.

    This very closely follows the logic of the :class:`agentpy.Model` package.

    Args:
        See :class:`agentpy.Model` for more information.
    """

    def __init__(self, parameters=None, _run_id=None, **kwargs):
        super().__init__(parameters, _run_id, **kwargs)
        self.env = Environment(self)

    def sim_step(self):

        self.t += 1

        for location in [location for location in self.locations if not location.static_weight]:
            location.update_weights()

        self.step()
        self.update()

        if self.t >= self._steps:  # type: ignore
            self.running = False

    def export_network(self) -> nx.Graph:

        agent_nodes = {n for n, d in self.env.g.nodes(data=True) if d["bipartite"] == 0}

        projection = bipartite.projection.projected_graph(self.env.g, agent_nodes)
        for agent_id in projection:
            del projection.nodes[agent_id]["_obj"]

        return projection

    def export_weighted_network(self) -> nx.Graph:
        projection = nx.Graph()

        for agent in self.agents:
            if not projection.has_node(agent.id):
                projection.add_node(agent.id)

            for agent_v in agent.neighbors():
                if not projection.has_edge(agent.id, agent_v.id):
                    projection.add_edge(agent.id, agent_v.id, weight=agent.contact_weight(agent_v))

        return projection
