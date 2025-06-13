import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "B"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 2
        only_exact_n_actors = True

        def weight(self, actor):
            return 1

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 1
    assert len(env.actors) == 3
    assert len(env.locations[0].actors) == 2
    assert all(actor.status == "A" for actor in env.locations[0].actors)
    assert all(env.locations[0].get_weight(actor) == 1 for actor in env.locations[0].actors)
