import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "B", "B", "B", "A", "A"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 2

        def split(self, actor):
            return actor.status

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 5
    assert len(env.actors) == 10
    for location in env.locations:
        if location.actors[0].status == "A":
            assert len(location.actors) == 2
            assert all(actor.status == "A" for actor in location.actors)
        if location.actors[0].status == "B":
            assert len(location.actors) == 2
            assert all(actor.status == "B" for actor in location.actors)


def test_2():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A"],
            "sex": ["m", "m", "m", "w"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 1

        def split(self, actor):
            return [actor.status, actor.sex]

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 8
    assert len(env.actors) == 4
    assert len(env.locations[0].actors) == 1
    assert len(env.locations[1].actors) == 1
    assert len(env.locations[2].actors) == 1
    assert len(env.locations[3].actors) == 1
    assert len(env.locations[4].actors) == 1
    assert len(env.locations[5].actors) == 1
    assert len(env.locations[6].actors) == 1
    assert len(env.locations[7].actors) == 1


def test_3():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A"],
            "sex": ["m", "m", "m", "w"],
        },
    )

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class TestLocation(p2n.LocationDesigner):
        n_actors = 1

        def split(self, actor):
            return str(actor.status) + str(actor.sex)

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(env.locations) == 4
    assert len(env.actors) == 4
    assert len(env.locations[0].actors) == 1
    assert len(env.locations[1].actors) == 1
    assert len(env.locations[2].actors) == 1
    assert len(env.locations[3].actors) == 1
