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

        # for location in self.locations:
        #    if hasattr(location, "update_weights"):
        #        location.update_weights()

        self.step()
        self.update()

        if self.t >= self._steps:  # type: ignore
            self.running = False

    def export_network(self) -> nx.Graph:

        agents, _ = bipartite.sets(self.env.g)

        projection = bipartite.projection.projected_graph(self.env.g, agents)
        for agent_id in projection:
            del projection.nodes[agent_id]["_obj"]

        return projection
