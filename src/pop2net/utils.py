"""Various utility functions for pop2net."""

from __future__ import annotations

import inspect
import typing

import numpy as np


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
    assert type(value) in [int, float], f"{value} has to be a number!"

    if value < start:
        new_value = np.nan

    else:
        for i in range(n_steps):
            lower_bound = start + step * i
            upper_bound = lower_bound + step

            if lower_bound <= value < upper_bound:
                break

        if return_value == "index":
            new_value = i

        elif return_value == "lower_bound":
            new_value = lower_bound

        elif return_value == "range":
            new_value = (lower_bound, upper_bound)

        if value >= upper_bound:
            if not summarize_highest:
                new_value = np.nan

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


def _to_list(x: object) -> list:
    return x if isinstance(x, list) else [x]


def _get_cls_as_str(cls_):
    # if isinstance(cls_, str):
    #    # if cls_ is a string
    #    return cls_
    if inspect.isclass(cls_):
        # if cls_ is a class
        return cls_.__name__
    else:
        # if cls_ is an instance
        return cls_.__class__.__name__


def _join_positions(pos1, pos2):
    return "-".join(sorted([str(pos1), str(pos2)]))
