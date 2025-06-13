import pytest

import pop2net as p2n


@pytest.fixture
def env():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class NormalLocation(p2n.LocationDesigner):
        pass

    class NormalLocation2(p2n.LocationDesigner):
        pass

    class MutationLocation(p2n.LocationDesigner):
        def mutate(self):
            return {"mutated1": [1, 2, 3], "mutated2": ["x", "y", "z"]}

    creator.create_actors(n=10)
    creator.create_locations(
        location_designers=[
            NormalLocation,
            MutationLocation,
            NormalLocation2,
        ]
    )
    return env


def test_n_locations(env):
    assert len(env.locations) == 11


def test_positions_and_labels(env):
    assert env.locations[0].label == "NormalLocation"
    assert env.locations[1].label == "MutationLocation0"
    assert env.locations[5].label == "MutationLocation4"
    assert env.locations[9].label == "MutationLocation8"
    assert env.locations[10].label == "NormalLocation2"


def test_mutated_values(env):
    assert env.locations[1].mutated1 == 1
    assert env.locations[1].mutated2 == "x"

    assert env.locations[5].mutated1 == 2
    assert env.locations[5].mutated2 == "y"

    assert env.locations[9].mutated1 == 3
    assert env.locations[9].mutated2 == "z"
