"""A module that helps with creating insights into the network."""

from __future__ import annotations

import typing

from bokehgraph import BokehGraph
import networkx as nx
import pandas as pd
from tabulate import tabulate

import popy.utils as utils

if typing.TYPE_CHECKING:
    from . import location as _location


class NetworkInspector:
    """Helper class that contains functions to inspect the network of a popy model."""

    def __init__(self, model) -> None:
        """Initiate a NetworkInspector.

        Args:
            model (Model): The model.
        """
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
                        graph.nodes[i][node_attr] = getattr(graph.nodes[i]["_obj"], node_attr)
                del graph.nodes[i]["_obj"]
            node_color = "type" if node_color is None else node_color

        elif network_type == "agent":
            graph = utils.create_agent_graph(
                agents=self.model.agents,
                node_attrs=node_attrs,
                include_0_weights=include_0_weights,
            )
            node_color = "type" if node_color is None else node_color

        graph_layout = nx.drawing.spring_layout(graph)
        plot = BokehGraph(graph, width=500, height=500, hover_edges=True)
        plot.layout(layout=graph_layout)
        plot.draw(
            node_color=node_color if network_type == "agent" else "type",
            edge_alpha="weight",
            edge_color="black",
            node_palette="random",
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
            node_attrs = ["type"]
        elif isinstance(node_attrs, list):
            if "type" not in node_attrs:
                node_attrs.append("type")
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

    def eval_affiliations(self, return_data=False) -> tuple[pd.DataFrame, pd.DataFrame] | None:
        """Prints information on the distribution of agents per location and locations per agent.

        Raises:
            PopyException: _description_
            PopyException: _description_
        """
        # if self.agents is None:
        #    msg = "You have to create agents first!"
        #    raise PopyException(msg)

        # if self.locations is None:
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
        return None

    #### Ported from utils #####
    def network_measures(self, node_attrs=None) -> dict | list[dict]:
        """Creates nx networkgraph and calculates common network measures.

        If the created network consist of independent groups of nodes
        subgraphs are created and measures are calculated for each subgraph

        Args:
            node_attrs: A list of agent attributes

        Return:
            dictionary/or list of dictionaries of the common network
            measure results
        """
        result_dict = {}
        nx_graph = utils.create_agent_graph(self.model.agents, node_attrs)

        # make distinction between multiple independent networks and one network
        if nx.is_connected(nx_graph):
            result_dict["diameter"] = nx.diameter(nx_graph, weight="weight")
            result_dict["density"] = nx.density(nx_graph)
            result_dict["transitivity"] = nx.transitivity(nx_graph)
            result_dict["avg_clustering"] = nx.average_clustering(
                nx_graph,
                weight="weight",
            )
            result_dict["avg_path_length"] = nx.average_shortest_path_length(
                nx_graph,
                weight="weight",
            )
            # result_dict["periphery"] = nx.periphery(nx_graph, weight = "weight")
            # result_dict["center"] = nx.center(nx_graph, weight = "weight")
            # result_dict["centrality"] = nx.degree_centrality(nx_graph)
            return result_dict
        else:
            # sort subgraph component size(=num of nodes) in ascending order
            component_list = sorted(
                nx.connected_components(nx_graph),
                key=len,
                reverse=False,
            )

            # create graph for each component and calculate network measures
            result_list = []
            for component in component_list:
                result_dict_subgraph = {}
                try:
                    nx_subgraph = nx_graph.subgraph(component)
                except nx.NetworkXError:
                    print("Cant make graph out of component")
                    break

                result_dict_subgraph["diameter"] = nx.diameter(
                    nx_subgraph,
                    weight="weight",
                )
                result_dict_subgraph["density"] = nx.density(nx_subgraph)
                result_dict_subgraph["transitivity"] = nx.transitivity(nx_subgraph)
                result_dict_subgraph["avg_clustering"] = nx.average_clustering(
                    nx_subgraph,
                    weight="weight",
                )
                result_dict_subgraph["avg_path_length"] = nx.average_shortest_path_length(
                    nx_subgraph,
                    weight="weight",
                )

                # result_dict_subgraph["centrality"] = nx.degree_centrality(nx_subgraph)
                # result_dict_subgraph["periphery"] = nx.periphery(nx_subgraph, weight = "weight")
                # result_dict_subgraph["center"] = nx.center(nx_subgraph, weight = "weight")
                result_list.append(result_dict_subgraph)
            return result_list

    ## TODO wie gebe ich hier den richtigen Datentyp an???
    def location_crosstab(
        self,
        select_locations: _location.location | list[_location.Location],
        agent_attributes: str | list[str],
        output_format="table",
    ) -> list[pd.DataFrame] | None:
        """Crosstable for specified location classes and agent attribute."""
        # Make every Parameter a list
        if select_locations:
            if not isinstance(select_locations, list):
                select_locations = [select_locations]

        if agent_attributes:
            if not isinstance(agent_attributes, list):
                agent_attributes = [agent_attributes]

        # determine eligible locations classes
        valid_locations = []
        if select_locations:
            for location_instance in self.model.locations:
                for locationtype in select_locations:
                    if isinstance(location_instance, locationtype):
                        valid_locations.append(location_instance)
        else:
            valid_locations = list(self.model.locations)

        # create agent df per location instance
        if output_format == "table":
            agent_dfs = {}
            if agent_attributes:
                for i, location_instance in enumerate(valid_locations):
                    title = f'{i+1}.Location: {str(location_instance).split(" ")[0]}'
                    df = pd.DataFrame([vars(agent) for agent in location_instance.agents])
                    df = df[list(agent_attributes)]
                    agent_dfs[title] = df

            for title, df in agent_dfs.items():
                for agent_attribute in agent_attributes:
                    crosstab_table = pd.crosstab(
                        index=df[agent_attribute],
                        columns="count",
                    )

                    print(f"{title}")
                    print(
                        tabulate(
                            crosstab_table,
                            headers=[agent_attribute, "count"],
                            tablefmt="fancy_grid",
                        ),
                    )
                    print("\n")
        if output_format == "df":
            agent_dfs = {}
            result_list = []
            for i, location_instance in enumerate(valid_locations):
                title = f'{i+1}.Location: {str(location_instance).split(" ")[0]}'
                location_type = str(location_instance).split(" ")[0]
                df = pd.DataFrame([vars(agent) for agent in location_instance.agents])

                # only keep wanted columns (agent attributes)
                df = df[list(agent_attributes)]

                # add location type as str
                df["location_type"] = location_type

                agent_dfs[title] = df

            for agent_attribute in agent_attributes:
                location_id = 0
                df_list_of_attribute = []
                for _, df in agent_dfs.items():
                    crosstab_table = pd.crosstab(
                        index=df[agent_attribute],
                        columns="count",
                    )
                    crosstab_table.insert(
                        0, "location_id", [location_id] * len(crosstab_table.index),
                    )
                    crosstab_table["location_type"] = df["location_type"][0]

                    df_list_of_attribute.append(crosstab_table)

                    location_id += 1
                df_attribute = pd.concat(df_list_of_attribute, ignore_index=False)

                # fix columns after concat
                df_attribute.reset_index(inplace=True)
                df_attribute.columns.names = ["index"]
                location_array = df_attribute["location_id"].copy()
                df_attribute.drop(columns="location_id", inplace=True)
                df_attribute.insert(0, "location_id", location_array)

                result_list.append(df_attribute)
            return result_list
        return None

    def location_information(
        self,
        select_locations: _location.Location | list[_location.Location] | None = None,
        agent_attributes: str | None | list[str] | None = None,
        output_format: str = "table",
    ) -> None | pd.DataFrame:
        """Provides information on the agents assigned to location instances.

           Displayed  information can be filtered by specifying certain location
           classes and agent_attributes

        Args:
            select_locations (popy.Location | list[popy.Location] | None, optional): A list of
                location classes. Defaults to None.
            agent_attributes (str | None | list[str] | None, optional): A list of agent attributes.
                Defaults to None.
            output_format (str, optional): A str determining what is returned. Defaults to "table".

        Returns:
            None | pd.DataFrame: A pandas.DataFrame or nothing.
        """
        if select_locations:
            if not isinstance(select_locations, list):
                select_locations = [select_locations]

        if agent_attributes:
            if not isinstance(agent_attributes, list):
                agent_attributes = [agent_attributes]

        # determine eligible locations classes
        valid_locations = []
        if select_locations:
            for location_instance in self.model.locations:
                for locationtype in select_locations:
                    if isinstance(location_instance, locationtype):
                        valid_locations.append(location_instance)
        else:
            valid_locations = list(self.model.locations)

        # create agent df per location instance
        agent_dfs = {}
        if agent_attributes:
            for i, location_instance in enumerate(valid_locations):
                # Create the title of printout
                title = f'{i+1}.Location: {str(location_instance).split(" ")[0]}'
                location_type = str(location_instance).split(" ")[0]
                # get all agents per location instance, subset df by agent-attributes
                df = pd.DataFrame([vars(agent) for agent in location_instance.agents])
                df = df[list(agent_attributes)]
                df["location_type"] = location_type
                agent_dfs[title] = df
        else:
            for i, location_instance in enumerate(valid_locations):
                title = f'{i+1}.Location: {str(location_instance).split(" ")[0]}'
                location_type = str(location_instance).split(" ")[0]
                df = pd.DataFrame([vars(agent) for agent in location_instance.agents])
                df.drop(df.iloc[:, 0:7], axis=1, inplace=True)
                df["location_type"] = location_type
                agent_dfs[title] = df

        if output_format == "table":
            #### Print Part "Basic"
            for title, df in agent_dfs.items():
                print(f"{title} \n")
                print(tabulate(df, headers="keys", tablefmt="fancy_grid"))
                print("\n")

        if output_format == "df":
            location_id_counter = 0
            df_list = []
            for _, df in agent_dfs.items():
                df.insert(0, "location_id", [location_id_counter] * len(df.index))
                location_id_counter += 1
                df_list.append(df)
            return pd.concat(df_list, ignore_index=True)
        return None
