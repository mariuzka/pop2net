import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "A", "B", "B", "B"],
        }
    )
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        only_exact_n_actors = False
        n_actors = 2

        def split(self, actor):
            return actor.status

    creator.create(df=df, location_designers=[TestLocation])

    assert len(env.actors) == 6
    assert len(env.locations) == 4
    assert len(env.locations[0].actors) == 2
    assert all(actor.status == "A" for actor in env.locations[0].actors)
    assert len(env.locations[1].actors) == 1
    assert all(actor.status == "A" for actor in env.locations[1].actors)
    assert len(env.locations[2].actors) == 2
    assert all(actor.status == "B" for actor in env.locations[2].actors)
    assert len(env.locations[3].actors) == 1
    assert all(actor.status == "B" for actor in env.locations[3].actors)

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        only_exact_n_actors = True
        n_actors = 2

        def split(self, actor):
            return actor.status

    creator.create(df=df, location_designers=[TestLocation])

    assert len(env.actors) == 6
    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 2
    assert all(actor.status == "A" for actor in env.locations[0].actors)
    assert len(env.locations[1].actors) == 2
    assert all(actor.status == "B" for actor in env.locations[1].actors)
    assert sum(not actor.locations for actor in env.actors if actor.status == "B") == 1
    assert sum(not actor.locations for actor in env.actors if actor.status == "A") == 1
