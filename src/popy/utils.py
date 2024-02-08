"""Various utility functions for popy."""
from __future__ import annotations

import typing

from bokehgraph import BokehGraph
import networkx as nx
from networkx import bipartite
import numpy as np
import pandas as pd
import seaborn as sns

if typing.TYPE_CHECKING:
    from popy import AgentList



##########################################################################
# scientific stuff
##########################################################################

def create_agent_graph(
        agents: AgentList,
        node_attrs: list | None = None,
        include_0_weights: bool = True,
) -> nx.Graph:
    """Create a Graph from a model's agent list.

    Args:
        agents: A model's agent list
        node_attrs: A list of agent attributes
        include_0_weights: Should edges with weight 0 be displayed?

    Returns:
        A weighted graph created from a model's agent list. Agents are connected if they are
        neighbors in the model. Their connecting edge include the contact_weight as "weight"
        attribute.
    """
    projection = nx.Graph()

    # create nodes
    for agent in agents:
        if not projection.has_node(agent.id):

            node_attr_dict = {}
            if node_attrs is not None:
                for node_attr in node_attrs:
                    node_attr_dict.update({node_attr: vars(agent)[node_attr]})
            projection.add_node(agent.id, **node_attr_dict)

    # create edges
    for agent in agents:
        for agent_v in agent.neighbors():
            if not projection.has_edge(agent.id, agent_v.id):
                weight = agent.contact_weight(agent_v)
                if include_0_weights or weight > 0:
                    projection.add_edge(agent.id, agent_v.id, weight=weight)

    return projection


def export_network(env) -> nx.Graph:
    """Export the current agent network (unweighted version).

    This is a projection of the underlying bipartite network between agents and locations.

    Returns:
        The current agent network as unipartite, unweighted graph.
    """
    agent_nodes = {n for n, d in env.g.nodes(data=True) if d["bipartite"] == 0}

    projection = bipartite.projection.projected_graph(env.g, agent_nodes)
    for agent_id in projection:
        del projection.nodes[agent_id]["_obj"]

    return projection


# TODO: calculate relative freqs
def create_contact_matrix(
    agents: list | AgentList,
    attr: str = "id",
    weighted: bool = False,
    plot: bool = False,
    annot: bool = False,
) -> pd.DataFrame:
    """Create a contact matrix as a DataFrame from a given model's agent list.

    Args:
        agents: A list of agents.
        attr: The agent attribute which is shown in the matrix.
        weighted: Should the contacts be weighted? Defaults to False.
        plot: Should the matrix be plotted? Defaults to False.
        annot: Should the plottet matrix be annotated? Defaults to False.

    Returns:
        A DataFrame containing a contact matrix based on `attr`.
    """
    contact_data = []
    attr_values = []
    pairs = []

    attr_u_name = f"{attr}_u"
    attr_v_name = f"{attr}_v"

    for agent_u in agents:
        attr_u = getattr(agent_u, attr)
        attr_values.append(attr_u)

        for agent_v in agent_u.neighbors():
            attr_v = getattr(agent_v, attr)
            attr_values.append(attr_v)

            pair = {agent_u.id, agent_v.id}

            if pair not in pairs:
                contact_data.append(
                    {
                        "id_u": agent_u.id,
                        attr_u_name: attr_u,
                        "id_v": agent_v.id,
                        attr_v_name: attr_v,
                        "weight": agent_u.contact_weight(agent_v),
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

    #df = df / 2

    if plot:
        g = sns.heatmap(df, annot=annot)
        g.set(xlabel=attr, ylabel=attr)

    return df


def eval_affiliations(agents, locations) -> None:
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

    df_locations = pd.DataFrame(
        [
            {
                "location_class": str(type(location)).split(".")[-1].split("'")[0],
                "n_agents": len(location.agents),
            }
            for location in locations
        ],
    )

    print_header("Number of agents per location")
    print(df_locations.groupby("location_class").describe())

    df_agents = pd.DataFrame(
        [
            {
                "agent_id": agent.id,
                "n_affiliated_locations": len(agent.locations),
            }
            for agent in agents
        ],
    )

    print_header("Number of affiliated locations per agent")
    print(df_agents.n_affiliated_locations.describe())


def plot_network(
        agents: list | AgentList,
        node_color: str = "red",
        node_attrs: list | None = None,
        edge_alpha: str = "weight",
        edge_color: str = "black",
        include_0_weights: bool = True,
):
    """_summary_.

    Args:
        agents (list | AgentList): _description_
        node_color (str, optional): _description_. Defaults to "red".
        node_attrs (list | None, optional): _description_. Defaults to None.
        edge_alpha (str, optional): _description_. Defaults to "weight".
        edge_color (str, optional): _description_. Defaults to "black".
        include_0_weights (bool, optional): _description_. Defaults to True.
    """
    graph = create_agent_graph(agents, node_attrs=node_attrs, include_0_weights=include_0_weights)
    graph_layout = nx.drawing.spring_layout(graph)
    plot = BokehGraph(graph, width=500, height=500, hover_edges=True)
    plot.layout(layout=graph_layout)
    plot.draw(
        node_color=node_color,
        edge_alpha=edge_alpha,
        edge_color=edge_color,
    )


##########################################################################
# technical helper functions
##########################################################################


def get_df_agents(agents: AgentList) -> pd.DataFrame:
    """_summary_.

    Args:
        agents (AgentList): _description_

    Returns:
        pd.DataFrame: _description_
    """
    return pd.DataFrame([vars(agent) for agent in agents])


def group_it(
    value: int | float,
    start: int | float,
    step: int,
    n_steps: int,
    return_value: typing.Literal["index", "lower_bound", "range"] = "index",
    summarize_highest: bool = False,
) -> int | float | tuple[int | float, int | float]:
    """_summary_.

    Args:
        value: _description_
        start: _description_
        step: _description_
        n_steps: _description_
        return_value: _description_. Defaults to "index".
        summarize_highest: _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    # TODO: something is fishy in this function...
    assert type(value) in [int, float], f"{value} has to be a number!"
    assert value >= start, f"The value {value} is smaller than the smallest lower bound {start}."

    for i in range(n_steps):
        lower_bound = start + step * i
        upper_bound = lower_bound + step

        if lower_bound <= value:
            if return_value == "index":
                new_value = i

            elif return_value == "lower_bound":
                new_value = lower_bound  # type: ignore

            elif return_value == "range":
                new_value = (lower_bound, upper_bound)  # type: ignore

            else:
                msg = "You have entered a non-existing option for `return_value`."
                raise Exception(msg)


        if not summarize_highest:
            if i == n_steps + 1:
                if value > upper_bound:
                    new_value = np.nan
    # BUG: new_value possibly unbound
    return new_value

def print_header(text: object):
    """Print a header around an object.

    Args:
        text: Object to be printed within the header.
    """
    # TODO: This is weird.... and it should probably not be print-statements cuz no one can catch
    # them.
    print("")
    print("")
    print("______________________________________")
    print(text)
    print("______________________________________")
    print("")


def network_measures(agent_list, node_attrs = None):
    """Creates nx networkgraph and calculates common network measures.

    If the created network consist of independent groups of nodes
    subgraphs are created and measures are calculated for each subgraph

    Args:
        agent_list: A model's agent list
        node_attrs: A list of agent attributes

    Return:
        dictionary/or list of dictionaries of the common network
        measure results
    """
    result_dict = {}
    nx_graph = create_agent_graph(agent_list, node_attrs)

    # make distinction between multiple independent networks and one network
    if nx.is_connected(nx_graph):

        result_dict["diameter"] = ntw_diameter(nx_graph)
        result_dict["density"] = ntw_density(nx_graph)
        result_dict["periphery"] = ntw_periphery(nx_graph)
        result_dict["center"] = ntw_center(nx_graph)
        result_dict["centrality"] = ntw_centrality(nx_graph)
        result_dict["avg_path_length"] = ntw_avg_path_length(nx_graph)
        return result_dict
    else:
        component_list = nx.connected_components(nx_graph)

        result_list = []
        for component in component_list:
            result_dict = {}
            try:
                nx_subgraph = nx_graph.subgraph(component)
            except nx.NetworkXError:
                print("Cant make graph out of component")
                break
            result_dict["diameter"] = ntw_diameter(nx_subgraph)
            result_dict["density"] = ntw_density(nx_subgraph)
            result_dict["periphery"] = ntw_periphery(nx_subgraph)
            result_dict["center"] = ntw_center(nx_subgraph)
            result_dict["centrality"] = ntw_centrality(nx_subgraph)
            result_dict["avg_path_length"] = ntw_avg_path_length(nx_subgraph)
            result_list.append(result_dict)
        return result_list


def ntw_diameter(nx_graph) -> int:
    """Calculates diameter of a graph."""
    return nx.diameter(nx_graph, weight = "weight")

def ntw_centrality(nx_graph) -> list:
    """Calculates centrality of a graph."""
    return nx.degree_centrality(nx_graph)

def ntw_density(nx_graph) -> float:
    """Calculates density of a graph."""
    return nx.density(nx_graph)

def ntw_avg_path_length(nx_graph) -> float:
   """Calculates average path lentgh of a graph."""
   return nx.average_shortest_path_length(nx_graph, weight = "weight")

def ntw_periphery(nx_graph) -> list:
    """Calculates periphery of a graph."""
    return nx.periphery(nx_graph, weight = "weight")

def ntw_center(nx_graph) -> list:
    """Calculates the center of a graph."""
    return nx.center(nx_graph, weight = "weight")

### Example for testing in introduction_static_networks (last example):
#result = utils.network_measures(agent_list=agents, node_attrs= df_school.columns)
