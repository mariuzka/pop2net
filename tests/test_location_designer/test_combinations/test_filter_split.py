import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B"],
            "sex": ["w", "m", "m", "m", "w"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocationA(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.status == "A"

        def split(self, actor):
            return actor.sex

    class TestLocationB(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.status == "B"

        def split(self, actor):
            return actor.sex

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocationA, TestLocationB])
    assert len(env.locations) == 4
    assert len(env.actors) == 5

    for location in env.locations:
        if location.type == "TestLocationA":
            assert all(actor.status == "A" for actor in location.actors)
        if location.type == "TestLocationB":
            assert all(actor.status == "B" for actor in location.actors)

    assert len(env.locations[0].actors) == 1
    assert len(env.locations[1].actors) == 1
    assert len(env.locations[2].actors) == 2
    assert len(env.locations[3].actors) == 1
    assert env.locations[0].actors[0].sex == "w"
    assert env.locations[1].actors[0].sex == "m"
    assert all(actor.sex == "m" for actor in env.locations[2].actors)
    assert all(actor.sex == "w" for actor in env.locations[3].actors)
