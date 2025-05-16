import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "A", "B"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocationA(p2n.LocationDesigner):
        n_actors = 2

        def filter(self, actor):
            return actor.status == "A"

    class TestLocationB(p2n.LocationDesigner):
        n_actors = 2

        def filter(self, actor):
            return actor.status == "B"

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocationA, TestLocationB])

    assert len(env.locations) == 4
    assert len(env.actors) == 7
    assert len(env.locations[0].actors) == 2
    assert len(env.locations[1].actors) == 1
    assert len(env.locations[2].actors) == 2
    assert len(env.locations[3].actors) == 2
    assert all(actor.status == "A" for actor in env.locations[0].actors)
    assert all(actor.status == "A" for actor in env.locations[1].actors)
    assert all(actor.status == "B" for actor in env.locations[2].actors)
    assert all(actor.status == "B" for actor in env.locations[3].actors)
