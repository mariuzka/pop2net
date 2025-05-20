import warnings

import networkx as nx
import pytest

import pop2net as p2n


def test_enable_warnings_true():
    env = p2n.Environment(enable_p2n_warnings=True)
    creator = p2n.Creator(env=env)

    class LineLocation(p2n.LocationDesigner):
        nxgraph = nx.path_graph(10)
        n_actors = 10

    creator.create_actors(n=10)

    with pytest.warns(UserWarning) as record:
        creator.create_locations(
            location_designers=[LineLocation],
            delete_magic_actor_attributes=False,
        )
    assert len(record) > 0, "Expected a warning but none were raised."


def test_enable_warnings_false():
    env = p2n.Environment(enable_p2n_warnings=False)
    creator = p2n.Creator(env=env)

    class LineLocation(p2n.LocationDesigner):
        nxgraph = nx.path_graph(10)
        n_actors = 10

    creator.create_actors(n=10)

    with warnings.catch_warnings(record=True) as record:
        warnings.simplefilter("always")
        creator.create_locations(
            location_designers=[LineLocation],
            delete_magic_actor_attributes=False,
        )
    assert len(record) == 0, "Expected no warnings but warnings were raised."
