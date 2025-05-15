# %%
import pandas as pd

import pop2net as p2n


# %%
def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "C"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 2

        def weight(self, actor):
            return 1

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.actors) == 6
    for location in env.locations:
        assert len(location.actors) == 2
        assert sum([location.get_weight(actor) for actor in location.actors]) == 2
        assert all(location.get_weight(actor) == 1 for actor in location.actors)


# %%
def test_2():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "C"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 2

        def weight(self, actor):
            if actor.status == "A":
                return 1
            if actor.status == "B":
                return 2
            if actor.status == "C":
                return 3

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 3
    assert len(env.actors) == 6
    sum_of_sum = 0
    for location in env.locations:
        sum_of_sum += sum([location.get_weight(actor) for actor in location.actors])
        assert len(location.actors) == 2
    assert sum_of_sum == 11
    for actor in env.actors:
        if actor.status == "A":
            assert actor.get_location_weight(actor.locations[0]) == 1
        if actor.status == "B":
            assert actor.get_location_weight(actor.locations[0]) == 2
        if actor.status == "C":
            assert actor.get_location_weight(actor.locations[0]) == 3


# %%
