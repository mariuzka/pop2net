"""Various utility functions for popy."""

from __future__ import annotations

import inspect
import typing

import numpy as np
import pandas as pd
import seaborn as sns

if typing.TYPE_CHECKING:
    from popy import AgentList


##########################################################################
# scientific stuff
##########################################################################


# TODO: calculate relative freqs
def create_contact_matrix(
    agents: list | AgentList,
    attr: str = "id",
    weighted: bool = False,
    plot: bool = True,
    annot: bool = False,
    return_df: bool = False,
) -> pd.DataFrame:
    """Create a contact matrix as a DataFrame from a given model's agent list.

    Args:
        agents: A list of agents.
        attr: The agent attribute which is shown in the matrix.
        weighted: Should the contacts be weighted? Defaults to False.
        plot: Should the matrix be plotted? Defaults to False.
        annot: Should the plottet matrix be annotated? Defaults to False.
        return_df: Should the data be returned as pandas.DataFrame?

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
        if attr_u is not None:
            attr_values.append(attr_u)

            for agent_v in agent_u.neighbors():
                attr_v = getattr(agent_v, attr)
                if attr_v is not None:
                    attr_values.append(attr_v)

                    pair = {agent_u.id, agent_v.id}

                    if pair not in pairs:
                        contact_data.append(
                            {
                                "id_u": agent_u.id,
                                attr_u_name: attr_u,
                                "id_v": agent_v.id,
                                attr_v_name: attr_v,
                                "weight": agent_u.get_agent_weight(agent_v),
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


##########################################################################
# technical helper functions
##########################################################################


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


def make_it_a_list_if_it_is_no_list(x: object) -> list:
    if isinstance(x, list):
        return x
    else:
        return [x]


def _get_cls_as_str(cls_):
    if inspect.isclass(cls_):
        # if cls_ is a class
        return cls_.__name__
    else:
        # if cls_ is an instance
        return cls_.__class__.__name__


def _join_positions(pos1, pos2):
    return "-".join(sorted([str(pos1), str(pos2)]))
