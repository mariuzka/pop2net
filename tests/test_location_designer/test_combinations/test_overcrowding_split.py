import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "B", "B", "A", "A", "A", "B", "B", "B", "A", "B", "A", "B"],
        },
    )

    class TestLocation1(p2n.LocationDesigner):
        overcrowding = None
        n_actors = 5

        def split(self, actor):
            return actor.status

    class TestLocation2(p2n.LocationDesigner):
        overcrowding = True
        n_actors = 5

        def split(self, actor):
            return actor.status

    class TestLocation3(p2n.LocationDesigner):
        overcrowding = False
        n_actors = 5

        def split(self, actor):
            return actor.status

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[TestLocation1])
    assert len(env.actors) == 14
    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 7
    assert len(env.locations[1].actors) == 7
    assert all(actor.status == "A" for actor in env.locations[0].actors)
    assert all(actor.status == "B" for actor in env.locations[1].actors)

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[TestLocation2])
    assert len(env.actors) == 14
    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 7
    assert len(env.locations[1].actors) == 7
    assert all(actor.status == "A" for actor in env.locations[0].actors)
    assert all(actor.status == "B" for actor in env.locations[1].actors)

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[TestLocation3])
    assert len(env.actors) == 14
    assert len(env.locations) == 4
    assert len(env.locations[0].actors) == 5
    assert len(env.locations[1].actors) == 2
    assert len(env.locations[2].actors) == 5
    assert len(env.locations[3].actors) == 2
    assert all(actor.status == "A" for actor in env.locations[0].actors)
    assert all(actor.status == "A" for actor in env.locations[1].actors)
    assert all(actor.status == "B" for actor in env.locations[2].actors)
    assert all(actor.status == "B" for actor in env.locations[3].actors)
