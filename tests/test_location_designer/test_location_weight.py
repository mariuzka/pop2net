import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        def weight(self, actor):
            return 1

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 1
    assert len(env.actors) == 5
    assert len(env.locations[0].actors) == 5
    # sum of weights correct?
    assert sum([env.get_weight(actor, env.locations[0]) for actor in env.locations[0].actors]) == 5
    # individual weights correct?
    assert all(env.get_weight(actor, env.locations[0]) == 1 for actor in env.locations[0].actors)


def test_2():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        def weight(self, actor):
            if actor.status == "A":
                return 1
            if actor.status == "B":
                return 5

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 1
    assert len(env.actors) == 5
    assert len(env.locations[0].actors) == 5
    # sum of weights correct?
    assert sum([env.get_weight(actor, env.locations[0]) for actor in env.locations[0].actors]) == 17
    # individual weights correct?
    assert all(
        env.get_weight(actor, env.locations[0]) == 1
        if actor.status == "A"
        else env.get_weight(actor, env.locations[0]) == 5
        for actor in env.locations[0].actors
    )


def test_3():
    df = pd.DataFrame(
        {
            "status": [1, 5, 5, 1, 5],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        def weight(self, actor):
            return actor.status

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 1
    assert len(env.actors) == 5
    assert len(env.locations[0].actors) == 5
    # sum of weights correct?
    assert sum([env.get_weight(actor, env.locations[0]) for actor in env.locations[0].actors]) == 17
    # individual weights correct?
    assert all(
        env.get_weight(actor, env.locations[0]) == 1
        if actor.status == 1
        else env.get_weight(actor, env.locations[0]) == 5
        for actor in env.locations[0].actors
    )
