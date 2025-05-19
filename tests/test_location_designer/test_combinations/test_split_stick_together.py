from collections import Counter

import pandas as pd

import pop2net as p2n


def test_1():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    df = pd.DataFrame(
        {
            "friend_group": [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4],
            "split_group": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        }
    )

    class TestLocation(p2n.LocationDesigner):
        n_actors = 4

        def split(self, actor):
            return actor.split_group

        def stick_together(self, actor):
            return actor.friend_group

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    for i, location in enumerate(env.locations):
        print(f"Location;{i}")
        [print(actor.friend_group) for actor in location.actors]

    assert len(env.locations) == 4
    assert len(env.actors) == 14
    # assert expecetd locations split and actor distribution
    for i, location in enumerate(env.locations):
        if i == 0:
            assert len(location.actors) == 4
            counter = Counter([actor.friend_group for actor in location.actors])
            assert list(counter.keys()) == [1, 2]
            assert list(counter.values()) == [2, 2]
        elif i == 1:
            assert len(location.actors) == 3
            counter = Counter([actor.friend_group for actor in location.actors])
            assert list(counter.keys()) == [3, 4]
            assert list(counter.values()) == [2, 1]
        elif i == 2:
            assert len(location.actors) == 4
            counter = Counter([actor.friend_group for actor in location.actors])
            assert list(counter.keys()) == [1, 2]
            assert list(counter.values()) == [2, 2]
        elif i == 3:
            assert len(location.actors) == 3
            counter = Counter([actor.friend_group for actor in location.actors])
            assert list(counter.keys()) == [3, 4]
            assert list(counter.values()) == [2, 1]
