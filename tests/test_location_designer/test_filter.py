import pandas as pd

import pop2net as p2n
from pop2net.creator import Creator


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B"],
        },
    )

    env = p2n.Environment()
    creator = Creator(env=env)

    class TestLocationA(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.status == "A"

    class TestLocationB(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.status == "B"

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocationA, TestLocationB])

    assert len(env.locations) == 2
    assert len(env.actors) == 5
    assert len(env.locations[0].actors) == 2
    assert len(env.locations[1].actors) == 3
    assert all(actor.status == "A" for actor in env.locations[0].actors)
    assert all(actor.status == "B" for actor in env.locations[1].actors)


def test_2():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B"],
            "sex": ["w", "m", "m", "m", "w"],
        },
    )

    env = p2n.Environment()
    creator = Creator(env)

    class TestLocationA(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.status == "A" and actor.sex == "w"

    class TestLocationB(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.status == "B" and actor.sex == "w"

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocationA, TestLocationB])

    assert len(env.locations) == 2
    assert len(env.actors) == 5
    assert len(env.locations[0].actors) == 1
    assert len(env.locations[1].actors) == 1
    assert all(actor.status == "A" and actor.sex == "w" for actor in env.locations[0].actors)
    assert all(actor.status == "B" and actor.sex == "w" for actor in env.locations[1].actors)
