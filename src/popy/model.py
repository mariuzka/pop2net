"""The model class. It encapsulates the full simulation."""

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
        """Initiate a simulation.

        Args:
            parameters (dict, optional): An optional parameter dict that is passed to
            :class:`agentpy.Model`. Defaults to None.
            _run_id (int, optional): An optional _run_id that is passed to :class:`agentpy.Model`.
            Defaults to None.
            **kwargs: Optional parameters that are all passed to :class:`agentpy.Model`.
        """
        super().__init__(parameters, _run_id, **kwargs)
        self.env = Environment(self)

    def sim_step(self):
        """Do 1 step in the simulation."""
        self.t += 1

        for location in [location for location in self.locations if not location.static_weight]:
            location.update_weights()

        self.step()
        self.update()

        if self.t >= self._steps:  # type: ignore
            self.running = False

    def export_network(self) -> nx.Graph:
        """Export the current agent network (unweighted version).

        This is a projection of the underlying bipartite network between agents and locations.

        Returns:
            nx.Graph: The current agent network as unipartite, unweighted networkx graph.
        """
        agent_nodes = {n for n, d in self.env.g.nodes(data=True) if d["bipartite"] == 0}

        projection = bipartite.projection.projected_graph(self.env.g, agent_nodes)
        for agent_id in projection:
            del projection.nodes[agent_id]["_obj"]

        return projection

    def export_weighted_network(self) -> nx.Graph:
        """Export the current agent network (weighted version).

        This is a projection of the underlying bipartite network between agents and locations.

        Returns:
            nx.Graph: The current agent network as unipartite, weighted networkx graph.
        """
        projection = nx.Graph()

        # BUG: This should be something like self.env.agents probably. The AgentList in the Model is
        # optional and might be different than the environment's.
        for agent in self.agents:
            if not projection.has_node(agent.id):
                projection.add_node(agent.id)

            for agent_v in agent.neighbors():
                if not projection.has_edge(agent.id, agent_v.id):
                    projection.add_edge(agent.id, agent_v.id, weight=agent.contact_weight(agent_v))

        return projection
