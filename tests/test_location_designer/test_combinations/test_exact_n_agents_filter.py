# %%
import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "A", "B"],
        }
    )
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        only_exact_n_actors = False
        n_actors = 2

        def filter(self, actor):
            return actor.status == "A"

    creator.create(df=df, location_designers=[TestLocation])

    assert len(env.actors) == 4
    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 2
    assert all(actor.status == "A" for actor in env.locations[0].actors)
    assert len(env.locations[1].actors) == 1
    assert all(actor.status == "A" for actor in env.locations[1].actors)
    assert all(not actor.locations for actor in env.actors if actor.status == "B")

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        only_exact_n_actors = True
        n_actors = 2

        def filter(self, actor):
            return actor.status == "A"

    creator.create(df=df, location_designers=[TestLocation])

    assert len(env.actors) == 4
    assert len(env.locations) == 1
    assert len(env.locations[0].actors) == 2
    assert all(actor.status == "A" for actor in env.locations[0].actors)
    assert all(not actor.locations for actor in env.actors if actor.status == "B")
