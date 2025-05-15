import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "C"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_locations = None

        def split(self, actor):
            return actor.status

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.actors) == 6
    assert TestLocation.n_locations is None


def test_2():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "C"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_locations = 3

        def split(self, actor):
            return actor.status

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.actors) == 6

    # check if the n_locations attribute is overwritten with None
    assert TestLocation.n_locations is None
