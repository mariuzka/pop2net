import pandas as pd

import pop2net as p2n


def test_create_agents():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    creator.create_actors(n=10, clear=False)

    assert len(env.actors) == 10

    creator.create_actors(n=10, clear=False)

    assert len(env.actors) == 20

    creator.create_actors(n=10, clear=True)

    assert len(env.actors) == 10


def test_create_locations():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class MyLocationDesigner(p2n.LocationDesigner):
        label = "MyLocation"
        n_locations = 5

    creator.create_actors(n=10)
    creator.create_locations(location_designers=[MyLocationDesigner], clear=False)

    assert len(env.actors) == 10
    assert len(env.locations) == 5

    creator.create_locations(location_designers=[MyLocationDesigner], clear=False)

    assert len(env.actors) == 10
    assert len(env.locations) == 10

    creator.create_locations(location_designers=[MyLocationDesigner], clear=True)

    assert len(env.actors) == 10
    assert len(env.locations) == 5


def test_create():
    df = pd.DataFrame({"age": [10, 20, 30, 40, 50]})

    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class MyLocationDesigner(p2n.LocationDesigner):
        label = "MyLocation"
        n_locations = 5

    creator.create(
        n_actors=10,
        df=df,
        location_designers=[MyLocationDesigner],
        clear=False,
    )

    assert len(env.actors) == 10
    assert len(env.locations) == 5

    creator.create(
        n_actors=10,
        df=df,
        location_designers=[MyLocationDesigner],
        clear=False,
    )

    assert len(env.actors) == 20
    assert len(env.locations) == 10

    creator.create(
        n_actors=10,
        df=df,
        location_designers=[MyLocationDesigner],
        clear=True,
    )

    assert len(env.actors) == 10
    assert len(env.locations) == 5
