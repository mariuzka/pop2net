from bokehgraph import BokehGraph
import networkx as nx
import popy.utils as utils
import pandas as pd

class NetworkInspector:
    def __init__(self, model) -> None:
        self.model = model

    def _plot_network(
        self,
        network_type,
        node_color: str | None,
        node_attrs: list | None,
        edge_alpha: str,
        edge_color: str,
        include_0_weights: bool,
    ):

        if network_type == "bipartite":
            graph = self.model.g.copy()
            for i in graph:
                if node_attrs is not None:
                    for node_attr in node_attrs:
                        graph.nodes[i][node_attr] = graph.nodes[i]["_obj"][node_attr]
                del graph.nodes[i]["_obj"]
            node_color = "cls" if node_color is None else node_color

        elif network_type == "agent":
            graph = utils.create_agent_graph(
                agents=self.model.agents,
                node_attrs=node_attrs,
                include_0_weights=include_0_weights,
            )
            node_color = "firebrick" if node_color is None else node_color

        graph_layout = nx.drawing.spring_layout(graph)
        plot = BokehGraph(graph, width=500, height=500, hover_edges=True)
        plot.layout(layout=graph_layout)
        plot.draw(
            node_color=node_color,
            edge_alpha=edge_alpha,
            edge_color=edge_color,
        )

    def plot_bipartite_network(
            self,
            node_color: str | None = None,
            node_attrs: list | None = None,
            edge_alpha: str = "weight",
            edge_color: str = "black",
            include_0_weights: bool = True,
    ) -> None:
        """Plots the two-mode network of agents and locations.

        Args:
            node_color (str, optional): The node attribute that determines the
                color of the nodes. If None, the node color represents whether
                it is a location or an agent instance.
            node_attrs (list | None, optional): A list of agent and location attributes that
                should be shown as node attributes in the network graph. Defaults to None.
            edge_alpha (str, optional): The node attribute that determines the edges' transparency.
                Defaults to "weight".
            edge_color (str, optional): The node attribute that determines the edges' color.
                Defaults to "black".
            include_0_weights (bool, optional): Should edges with a weight of zero be included in
                the plot? Defaults to True.
        """
        if node_attrs is None:
            node_attrs = ["cls"]
        elif isinstance(node_attrs, list):
            if "cls" not in node_attrs:
                node_attrs.append(node_attrs)
        else:
            raise Exception

        self._plot_network(
            network_type="bipartite",
            node_color=node_color,
            node_attrs=node_attrs,
            edge_alpha=edge_alpha,
            edge_color=edge_color,
            include_0_weights=include_0_weights,
        )

    def plot_agent_network(
            self,
            node_color: str | None = "firebrick",
            node_attrs: list | None = None,
            edge_alpha: str = "weight",
            edge_color: str = "black",
            include_0_weights: bool = True,
    ) -> None:
        """Plots the agent network.

        Args:
            node_color (str, optional): The node attribute that determines the
                color of the nodes. If None, the node color represents whether
                it is a location or an agent instance.
            node_attrs (list | None, optional): A list of agent and location attributes that
                should be shown as node attributes in the network graph. Defaults to None.
            edge_alpha (str, optional): The node attribute that determines the edges' transparency.
                Defaults to "weight".
            edge_color (str, optional): The node attribute that determines the edges' color.
                Defaults to "black".
            include_0_weights (bool, optional): Should edges with a weight of zero be included in
                the plot? Defaults to True.
        """
        self._plot_network(
            network_type="agent",
            node_color=node_color,
            node_attrs=node_attrs,
            edge_alpha=edge_alpha,
            edge_color=edge_color,
            include_0_weights=include_0_weights,
        )
    

    def eval_affiliations(self, return_data=False) -> None:
        """Prints information on the distribution of agents per location and locations per agent.

        Raises:
            PopyException: _description_
            PopyException: _description_
        """
        #if self.agents is None:
        #    msg = "You have to create agents first!"
        #    raise PopyException(msg)

        #if self.locations is None:
        #    msg = "You have to create locations first!"
        #    raise PopyException(msg)

        df1 = pd.DataFrame(
            [
                {
                    "location_class": str(type(location)).split(".")[-1].split("'")[0],
                    "n_agents": len(location.agents),
                }
                for location in self.model.locations
            ],
        )

        df1 = df1.groupby("location_class").describe()
        df1.columns = df1.columns.droplevel()
        df1 = df1.drop("count", axis=1)
        

        utils.print_header("Number of agents per location")
        print(df1)

        df2 = pd.DataFrame(
            [
                {
                    "agent_id": agent.id,
                    "n_affiliated_locations": len(agent.locations),
                }
                for agent in self.model.agents
            ],
        )
        df2 = df2.n_affiliated_locations.describe()
        df2 = df2.drop("count", axis=0)

        utils.print_header("Number of affiliated locations per agent")
        print(df2)

        if return_data:
            return df1, df2