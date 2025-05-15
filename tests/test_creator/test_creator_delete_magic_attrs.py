import pandas as pd
import pytest

import pop2net as p2n


@pytest.fixture(scope="session")
def magic_actor_attributes():
    magic_actor_attributes = ["", "_assigned", "_id", "_position", "_head", "_tail"]
    magic_actor_attributes = ["Location1" + attr for attr in magic_actor_attributes] + [
        "Location2" + attr for attr in magic_actor_attributes
    ]
    return magic_actor_attributes


def test_del_magic_agent_attrs1(magic_actor_attributes):
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class Location1(p2n.LocationDesigner):
        pass

    class Location2(p2n.LocationDesigner):
        pass

    # First test: Do NOT delete magic agent attributes
    creator.create_actors(n=10)
    creator.create_locations(
        location_designers=[Location1, Location2],
        delete_magic_actor_attributes=False,
    )

    for actor in env.actors:
        for attr in magic_actor_attributes:
            assert hasattr(actor, attr)

    # Second test: DELETE magic agent attributes
    creator.create_actors(n=10, clear=True)
    creator.create_locations(
        location_designers=[Location1, Location2],
        delete_magic_actor_attributes=True,
        clear=True,
    )

    for agent in env.actors:
        for attr in magic_actor_attributes:
            assert not hasattr(actor, attr)


def test_del_magic_agent_attrs2(magic_actor_attributes):
    df = pd.DataFrame({"testattr": [10, 11, 12, 13]})

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class Location1(p2n.LocationDesigner):
        pass

    class Location2(p2n.LocationDesigner):
        pass

    # First test: Do NOT delete magic agent attributes
    creator.create(
        df=df,
        n_actors=10,
        location_designers=[Location1, Location2],
        delete_magic_actor_attributes=False,
    )

    for actor in env.actors:
        for attr in magic_actor_attributes:
            assert hasattr(actor, attr)

    # Second test: DELETE magic agent attributes
    creator.create(
        df=df,
        n_agents=10,
        location_designers=[Location1, Location2],
        delete_magic_actor_attributes=True,
        clear=True,
    )

    for actor in env.actors:
        for attr in magic_actor_attributes:
            assert not hasattr(actor, attr)
