"""Various utility functions for popy."""
from __future__ import annotations

import typing
from typing import Optional, List
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns

from . import agent as _agent

if typing.TYPE_CHECKING:
    from popy import AgentList


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


def create_agent_graph(agents: AgentList, node_attrs: List = []) -> nx.Graph:
    """Create a Graph from a model's agent list.

    Args:
        agents: A model's agent list

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
            for node_attr in node_attrs:
                node_attr_dict.update({node_attr: vars(agent)[node_attr]})
            projection.add_node(agent.id, **node_attr_dict)

    # create edges
    for agent in agents:
        for agent_v in agent.neighbors():
            if not projection.has_edge(agent.id, agent_v.id):
                projection.add_edge(agent.id, agent_v.id, weight=agent.contact_weight(agent_v))

    return projection

# TODO: calculate relative freqs
def create_contact_matrix(
    agents,
    attr: str = "id",
    weighted: bool = False,
    plot: bool = False,
    annot: bool = False,
) -> pd.DataFrame:
    """Create a contact matrix as a DataFrame from a given model's agent list.

    Args:
        agents: _description_
        attr: _description_. Defaults to "id".
        weighted: _description_. Defaults to False.
        plot: _description_. Defaults to False.

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

def get_df_agents(agents: AgentList) -> pd.DataFrame:
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

        if not summarize_highest:
            if i == n_steps + 1:
                if value > upper_bound:
                    new_value = np.nan
    # BUG: new_value possibly unbound
    return new_value
