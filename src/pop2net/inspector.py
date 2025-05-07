"""A module that helps with creating insights into the network."""

from __future__ import annotations

import typing

from bokehgraph import BokehGraph
import networkx as nx
import pandas as pd
import seaborn as sns
from tabulate import tabulate

import pop2net.utils as utils

if typing.TYPE_CHECKING:
    from . import location as _location


class NetworkInspector:
    """Helper class that contains functions to inspect the network of a pop2net environment."""

    def __init__(self, env) -> None:
        """Initiate a NetworkInspector.

        Args:
            env (Environment): The environment this NetworkInspector belongs to.
        """
        self.env = env  # TODO: make instances of inspector without a fixed env possible

    def plot_bipartite_network(
        self,
        actor_attrs: list | None = None,
        location_attrs: list | None = None,
        actor_color: str | None = None,
        location_color: str | None = None,
        edge_alpha: str = "weight",
        edge_color: str = "black",
        edge_size: int = 1,
        node_size: int = 10,
        node_alpha=0.5,
    ) -> None:
        """Plots the bipartite network of actors and locations.

        Args:
            actor_attrs (list | None, optional): A list of actor attributes that
                should be shown as node attributes in the network graph. Defaults to None.
            location_attrs (list | None, optional): A list of location attributes that
                should be shown as node attributes in the network graph. Defaults to None.
            actor_color (str | None, optional): The actor attribute that determines the
            color of the actor nodes. Defaults to None.
            location_color (str | None, optional): The location attribute that determines the
            color of the location nodes. Defaults to None.
            edge_alpha (str, optional): The edge attribute that determines the edges' transparency.
                Defaults to "weight".
            edge_color (str, optional): The color of the edges. Defaults to "black".
            edge_size (int, optional): The size of the edges. Defaults to 1.
            node_size (int, optional): The size of the nodes. Defaults to 10.
            node_alpha (float, optional): The transparency of the nodes. Defaults to 0.5.
        """
        # if actor_attrs is None:
        #    actor_attrs = ["type"]
        # else:
        #    actor_attrs = list(actor_attrs)
        #    if "type" not in actor_attrs:
        #        actor_attrs.append("type")

        if actor_color is not None and actor_color not in actor_attrs:
            actor_attrs.append(actor_color)

        # if location_attrs is None:
        #    location_attrs = ["type", "label"]
        # else:
        #    location_attrs = list(location_attrs)
        #    if "type" not in location_attrs:
        #        location_attrs.append("type")

        #    if "label" not in location_attrs:
        #        location_attrs.append("label")

        if location_color is not None and location_color not in location_attrs:
            location_attrs.append(location_color)

        graph = self.env.export_bipartite_network(
            actor_attrs=actor_attrs,
            location_attrs=location_attrs,
        )

        graph_layout = nx.drawing.spring_layout(graph)
        plot = BokehGraph(
            graph,
            width=400,
            height=400,
            hover_edges=True,
            bipartite=True,
        )
        plot.layout(layout=graph_layout)

        plot.draw(
            node_color=(
                actor_color if actor_color is not None else "firebrick",
                location_color if location_color is not None else "steelblue",
            ),
            edge_alpha=edge_alpha,
            edge_color=edge_color,
            edge_size=edge_size,
            node_size=node_size,
            node_alpha=node_alpha,
        )

    def plot_actor_network(
        self,
        actor_color: str | None = None,
        actor_attrs: list | None = None,
        edge_alpha: str = "weight",
        edge_color: str = "black",
        include_0_weights: bool = True,
        edge_size: int = 1,
        node_size: int = 10,
        node_alpha=0.5,
    ) -> None:
        """Plots the actor network.

        Args:
            actor_color (str | None, optional): The actor attribute that determines the
            color of the actor nodes. Defaults to None.
            actor_attrs (list | None, optional): A list of actor attributes that
                should be shown as node attributes in the network graph. Defaults to None.
            edge_alpha (str, optional): The edge attribute that determines the edges' transparency.
                Defaults to "weight".
            edge_color (str, optional): The color of the edges. Defaults to "black".
            include_0_weights (bool, optional): Should edges with a weight of zero be included in
                the plot? Defaults to True.
            edge_size (int, optional): The size of the edges. Defaults to 1.
            node_size (int, optional): The size of the nodes. Defaults to 10.
            node_alpha (float, optional): The transparency of the nodes. Defaults to 0.5.
        """
        # if actor_attrs is None:
        #    actor_attrs = ["type"]
        # else:
        #    actor_attrs = list(actor_attrs)
        #    if "type" not in actor_attrs:
        #        actor_attrs.append("type")

        if actor_color is not None and actor_color not in actor_attrs:
            actor_attrs.append(actor_color)

        graph = self.env.export_actor_network(
            node_attrs=actor_attrs,
            include_0_weights=include_0_weights,
        )

        graph_layout = nx.drawing.spring_layout(graph)
        plot = BokehGraph(graph, width=400, height=400, hover_edges=True)
        plot.layout(layout=graph_layout)
        plot.draw(
            node_color="firebrick" if actor_color is None else actor_color,
            node_size=node_size,
            edge_alpha=edge_alpha,
            edge_color=edge_color,
            edge_size=edge_size,
            node_alpha=node_alpha,
        )

    def plot_networks(
        self,
        actor_attrs: list | None = None,
        location_attrs: list | None = None,
        actor_color: str | None = None,
        location_color: str | None = None,
        edge_alpha: str = "weight",
        edge_color: str = "black",
        include_0_weights: bool = True,
        edge_size: int = 1,
        node_size: int = 10,
        node_alpha: float = 0.5,
    ) -> None:
        """Plots the bipartite network and the actor network.

        Args:
            actor_attrs (list | None, optional): A list of actor attributes that
                should be shown as node attributes in the network graph. Defaults to None.
            location_attrs (list | None, optional): A list of location attributes that
                should be shown as node attributes in the network graph. Defaults to None.
            actor_color (str | None, optional): The actor attribute that determines the
                color of the actor nodes. Defaults to None.
            location_color (str | None, optional): The location attribute that determines the
                color of the location nodes. Defaults to None.
            edge_alpha (str, optional): The edge attribute that determines the edges' transparency.
                Defaults to "weight".
            edge_color (str, optional): The color of the edges. Defaults to "black".
            include_0_weights (bool, optional): Should edges with a weight of zero be included in
                the plot? Defaults to True.
            edge_size (int, optional): The size of the edges. Defaults to 1.
            node_size (int, optional): The size of the nodes. Defaults to 10.
            node_alpha (float, optional): The transparency of the nodes. Defaults to 0.5.
        """
        self.plot_bipartite_network(
            actor_color=actor_color,
            actor_attrs=actor_attrs,
            location_color=location_color,
            location_attrs=location_attrs,
            edge_color=edge_color,
            edge_alpha=edge_alpha,
            edge_size=edge_size,
            node_size=node_size,
            node_alpha=node_alpha,
        )

        self.plot_actor_network(
            actor_color=actor_color,
            actor_attrs=actor_attrs,
            edge_color=edge_color,
            edge_alpha=edge_alpha,
            include_0_weights=include_0_weights,
            edge_size=edge_size,
            node_size=node_size,
            node_alpha=node_alpha,
        )

    def eval_affiliations(self, return_data=False) -> tuple[pd.DataFrame, pd.DataFrame] | None:
        """Prints information on the distribution of actors per location and locations per actor.

        Raises:
            Pop2netException: _description_
            Pop2netException: _description_
        """
        df1 = pd.DataFrame(
            [
                {
                    "location_label": location.label,
                    "n_actors": len(location.actors),
                }
                for location in self.env.locations
            ],
        )

        utils.print_header("Number of locations")
        print(df1.location_label.value_counts().to_frame())

        df1 = df1.groupby("location_label").describe()
        df1.columns = df1.columns.droplevel()
        df1 = df1.drop("count", axis=1)

        utils.print_header("Number of actors per location")
        print(df1)

        df2 = pd.DataFrame(
            [
                {
                    "actor_id": actor.id,
                    "n_affiliated_locations": len(actor.locations),
                }
                for actor in self.env.actors
            ],
        )
        df2 = df2.n_affiliated_locations.describe()
        df2 = df2.drop("count", axis=0)

        utils.print_header("Number of affiliated locations per actor")
        print(df2.to_frame())

        if return_data:
            return df1, df2
        return None

    # TODO: calculate relative freqs
    def create_contact_matrix(
        self,
        actors: list | None = None,
        attr: str = "id",
        weighted: bool = False,
        plot: bool = True,
        annot: bool = False,
        return_df: bool = False,
    ) -> pd.DataFrame:
        """Create a contact matrix as a DataFrame from a given env's actor list.

        Args:
            actors: A list of actors.
            attr: The actor attribute which is shown in the matrix.
            weighted: Should the contacts be weighted? Defaults to False.
            plot: Should the matrix be plotted? Defaults to False.
            annot: Should the plottet matrix be annotated? Defaults to False.
            return_df: Should the data be returned as pandas.DataFrame?

        Returns:
            A DataFrame containing a contact matrix based on `attr`.
        """
        if actors is None:
            actors = self.env.actors

        contact_data = []
        attr_values = []
        pairs = []

        attr_u_name = f"{attr}_u"
        attr_v_name = f"{attr}_v"

        for actor_u in actors:
            attr_u = getattr(actor_u, attr)
            if attr_u is not None:
                attr_values.append(attr_u)

                for actor_v in actor_u.neighbors():
                    attr_v = getattr(actor_v, attr)
                    if attr_v is not None:
                        attr_values.append(attr_v)

                        pair = {actor_u.id, actor_v.id}

                        if pair not in pairs:
                            contact_data.append(
                                {
                                    "id_u": actor_u.id,
                                    attr_u_name: attr_u,
                                    "id_v": actor_v.id,
                                    attr_v_name: attr_v,
                                    "weight": actor_u.get_actor_weight(actor_v),
                                },
                            )
                            pairs.append(pair)

        attr_values = list(set(attr_values))

        df = pd.DataFrame(index=sorted(attr_values, reverse=True), columns=sorted(attr_values))
        df = df.fillna(0)

        weight_total = 0
        for contact in contact_data:
            weight = contact["weight"] if weighted else 1
            weight_total += weight

            df.loc[contact[attr_u_name], contact[attr_v_name]] = (
                df.loc[contact[attr_u_name], contact[attr_v_name]] + weight
            )
            df.loc[contact[attr_v_name], contact[attr_u_name]] = (
                df.loc[contact[attr_v_name], contact[attr_u_name]] + weight
            )

        if plot:
            g = sns.heatmap(df, annot=annot, vmin=0, fmt="g")
            g.set(xlabel=attr, ylabel=attr)

        if return_df:
            return df

    def network_measures(self, actor_attrs=None) -> list[dict]:
        """Calculates common network measures for the actor-level network graph.

        If the created network consist of independent groups of nodes
        subgraphs are created and measures are calculated for each subgraph

        Args:
            actor_attrs: A list of actor attributes

        Return:
            list of dictionaries of the common network measure results
        """
        nx_graph = self.env.export_actor_network(node_attrs=actor_attrs)

        # make distinction between multiple independent networks and one network

        def get_network_measures(nx_graph) -> dict:
            result_dict = {}
            result_dict["n_nodes"] = nx.number_of_nodes(nx_graph)
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
            return result_dict

        network_components = list(nx.connected_components(nx_graph))
        network_components = sorted(network_components, key=len, reverse=True)

        # create graph for each component and calculate network measures
        result_list = []
        for component in network_components:
            try:
                nx_subgraph = nx_graph.subgraph(component)
            except nx.NetworkXError:
                print("Cant make graph out of component")
                break

            result_list.append(get_network_measures(nx_subgraph))
        return result_list

    def location_crosstab(
        self,
        select_locations: _location.location | list[_location.Location],
        actor_attributes: str | list[str],
        output_format="table",
    ) -> list[pd.DataFrame] | None:
        """Crosstable for specified location classes and actor attribute."""
        # Make every Parameter a list
        if select_locations:
            if not isinstance(select_locations, list):
                select_locations = [select_locations]

        if actor_attributes:
            if not isinstance(actor_attributes, list):
                actor_attributes = [actor_attributes]

        # determine eligible locations classes
        valid_locations = []
        if select_locations:
            for location_instance in self.env.locations:
                for locationtype in select_locations:
                    if isinstance(location_instance, locationtype):
                        valid_locations.append(location_instance)
        else:
            valid_locations = list(self.env.locations)

        # create actor df per location instance
        if output_format == "table":
            actor_dfs = {}
            if actor_attributes:
                for i, location_instance in enumerate(valid_locations):
                    title = f"{i + 1}.Location: {str(location_instance).split(' ')[0]}"
                    df = pd.DataFrame([vars(actor) for actor in location_instance.actors])
                    df = df[list(actor_attributes)]
                    actor_dfs[title] = df

            for title, df in actor_dfs.items():
                for actor_attribute in actor_attributes:
                    crosstab_table = pd.crosstab(
                        index=df[actor_attribute],
                        columns="count",
                    )

                    print(f"{title}")
                    print(
                        tabulate(
                            crosstab_table,
                            headers=[actor_attribute, "count"],
                            tablefmt="fancy_grid",
                        ),
                    )
                    print("\n")
        if output_format == "df":
            actor_dfs = {}
            result_list = []
            for i, location_instance in enumerate(valid_locations):
                title = f"{i + 1}.Location: {str(location_instance).split(' ')[0]}"
                location_type = str(location_instance).split(" ")[0]
                df = pd.DataFrame([vars(actor) for actor in location_instance.actors])

                # only keep wanted columns (actor attributes)
                df = df[list(actor_attributes)]

                # add location type as str
                df["location_type"] = location_type

                actor_dfs[title] = df

            for actor_attribute in actor_attributes:
                location_id = 0
                df_list_of_attribute = []
                for _, df in actor_dfs.items():
                    crosstab_table = pd.crosstab(
                        index=df[actor_attribute],
                        columns="count",
                    )
                    crosstab_table.insert(
                        0,
                        "location_id",
                        [location_id] * len(crosstab_table.index),
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
        actor_attributes: str | None | list[str] | None = None,
        output_format: str = "table",
    ) -> None | pd.DataFrame:
        """Provides information on the actors assigned to location instances.

           Displayed  information can be filtered by specifying certain location
           classes and actor_attributes

        Args:
            select_locations (p2n.Location | list[p2n.Location] | None, optional): A list of
                location classes. Defaults to None.
            actor_attributes (str | None | list[str] | None, optional): A list of actor attributes.
                Defaults to None.
            output_format (str, optional): A str determining what is returned. Defaults to "table".

        Returns:
            None | pd.DataFrame: A pandas.DataFrame or nothing.
        """
        if select_locations:
            if not isinstance(select_locations, list):
                select_locations = [select_locations]

        if actor_attributes:
            if not isinstance(actor_attributes, list):
                actor_attributes = [actor_attributes]

        # determine eligible locations classes
        valid_locations = []
        if select_locations:
            for location_instance in self.env.locations:
                for locationtype in select_locations:
                    if isinstance(location_instance, locationtype):
                        valid_locations.append(location_instance)
        else:
            valid_locations = list(self.env.locations)

        # create actor df per location instance
        actor_dfs = {}
        if actor_attributes:
            for i, location_instance in enumerate(valid_locations):
                # Create the title of printout
                title = f"{i + 1}.Location: {str(location_instance).split(' ')[0]}"
                location_type = str(location_instance).split(" ")[0]
                # get all actors per location instance, subset df by actor-attributes
                df = pd.DataFrame([vars(actor) for actor in location_instance.actors])
                df = df[list(actor_attributes)]
                df["location_type"] = location_type
                actor_dfs[title] = df
        else:
            for i, location_instance in enumerate(valid_locations):
                title = f"{i + 1}.Location: {str(location_instance).split(' ')[0]}"
                location_type = str(location_instance).split(" ")[0]
                df = pd.DataFrame([vars(actor) for actor in location_instance.actors])
                df.drop(df.iloc[:, 0:7], axis=1, inplace=True)
                df["location_type"] = location_type
                actor_dfs[title] = df

        if output_format == "table":
            #### Print Part "Basic"
            for title, df in actor_dfs.items():
                print(f"{title} \n")
                print(tabulate(df, headers="keys", tablefmt="fancy_grid"))
                print("\n")

        if output_format == "df":
            location_id_counter = 0
            df_list = []
            for _, df in actor_dfs.items():
                df.insert(0, "location_id", [location_id_counter] * len(df.index))
                location_id_counter += 1
                df_list.append(df)
            return pd.concat(df_list, ignore_index=True)
        return None
