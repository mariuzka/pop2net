import pandas as pd

import pop2net as p2n


# TODO ohne n_actors oder n_locations seh ich keine Möglichkeit stick_together mit filter sinnvoll zu testen
def test_1():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    df = pd.DataFrame(
        {"friend_group": [1, 2, 2, 3, 1, 3, 2], "filter_group": [1, 1, 2, 2, 1, 1, 2]}
    )

    class TestLocationA(p2n.LocationDesigner):
        n_actors = 2

        def filter(self, actor):
            return actor.filter_group == 1

        def stick_together(self, actor):
            return actor.friend_group

    class TestLocationB(p2n.LocationDesigner):
        n_actors = 2

        def filter(self, actor):
            return actor.filter_group == 2

        def stick_together(self, actor):
            return actor.friend_group

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocationA, TestLocationB])

    assert len(env.locations) == 4
    assert len(env.actors) == 7
    assert len([location for location in env.locations if location.label == "TestLocationA"]) == 2
    assert len([location for location in env.locations if location.label == "TestLocationB"]) == 2

    assert len(env.locations[0].actors) == 2
    assert all(actor.friend_group == 1 for actor in env.locations[0].actors)
    assert len(env.locations[1].actors) == 2
    assert all(actor.friend_group in [2, 3] for actor in env.locations[1].actors)
    assert len(env.locations[2].actors) == 2
    assert all(actor.friend_group == 2 for actor in env.locations[2].actors)
    assert len(env.locations[3].actors) == 1
    assert all(actor.friend_group == 3 for actor in env.locations[3].actors)
