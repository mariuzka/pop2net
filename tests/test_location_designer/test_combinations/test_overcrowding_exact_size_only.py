import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "A", "A", "A", "A", "A"],
        },
    )

    class TestLocation(p2n.LocationDesigner):
        overcrowding = None
        n_actors = 5
        only_exact_n_actors = False

    class TestLocation2(p2n.LocationDesigner):
        overcrowding = True
        n_actors = 5
        only_exact_n_actors = False

    class TestLocation3(p2n.LocationDesigner):
        overcrowding = False
        n_actors = 5
        only_exact_n_actors = False

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[TestLocation])

    assert len(env.actors) == 7
    assert len(env.locations) == 1
    assert len(env.locations[0].actors) == 7

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[TestLocation2])

    assert len(env.actors) == 7
    assert len(env.locations) == 1
    assert len(env.locations[0].actors) == 7

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[TestLocation3])

    assert len(env.actors) == 7
    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 5
    assert len(env.locations[1].actors) == 2


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "A", "A", "A", "A", "A"],
        },
    )

    class TestLocation(p2n.LocationDesigner):
        overcrowding = None
        n_actors = 5
        only_exact_n_actors = True

    class TestLocation2(p2n.LocationDesigner):
        overcrowding = True
        n_actors = 5
        only_exact_n_actors = True

    class TestLocation3(p2n.LocationDesigner):
        overcrowding = False
        n_actors = 5
        only_exact_n_actors = True

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[TestLocation])

    assert len(env.actors) == 7
    assert len(env.locations) == 1
    assert len(env.locations[0].actors) == 5
    assert sum(not actor.locations for actor in env.actors) == 2

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[TestLocation2])

    assert len(env.actors) == 7
    assert len(env.locations) == 1
    assert len(env.locations[0].actors) == 5
    assert sum(not actor.locations for actor in env.actors) == 2

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[TestLocation3])

    assert len(env.actors) == 7
    assert len(env.locations) == 1
    assert len(env.locations[0].actors) == 5
    assert sum(not actor.locations for actor in env.actors) == 2
