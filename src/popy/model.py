import agentpy as ap
import networkx as nx
from networkx import bipartite


class Model(ap.Model):
    """Class the encapsulates a full simluation.

    This very closely follows the logic of the :class:`agentpy.Model` package.

    Args:
        See :agentpy.Model: for more information.
    """

    def __init__(self, parameters=None, _run_id=None, **kwargs):
        super().__init__(parameters, _run_id, **kwargs)

    def sim_step(self):

        self.t += 1

        self.agents.visit_locations()

        self.locations.update()

        self.step()
        self.update()

        if self.t >= self._steps:  # type: ignore
            self.running = False

    def export_network(self) -> nx.Graph:

        comp_graph = nx.compose_all(location.graph.g for location in self.locations)
        _, agents = bipartite.sets(comp_graph)

        projection = bipartite.projection.projected_graph(comp_graph, agents)
        for agent_id in projection:
            del projection.nodes[agent_id]["_agent"]

        return projection
