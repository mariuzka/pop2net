import pandas as pd

import pop2net as p2n


def test_create_agents():
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    creator.create_agents(n=10, clear=False)

    assert len(model.agents) == 10

    creator.create_agents(n=10, clear=False)

    assert len(model.agents) == 20

    creator.create_agents(n=10, clear=True)

    assert len(model.agents) == 10


def test_create_locations():
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class MyLocationDesigner(p2n.LocationDesigner):
        label = "MyLocation"
        n_locations = 5

    creator.create_agents(n=10)
    creator.create_locations(location_designers=[MyLocationDesigner], clear=False)

    assert len(model.agents) == 10
    assert len(model.locations) == 5

    creator.create_locations(location_designers=[MyLocationDesigner], clear=False)

    assert len(model.agents) == 10
    assert len(model.locations) == 10

    creator.create_locations(location_designers=[MyLocationDesigner], clear=True)

    assert len(model.agents) == 10
    assert len(model.locations) == 5


def test_create():
    df = pd.DataFrame({"age": [10, 20, 30, 40, 50]})

    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class MyLocationDesigner(p2n.LocationDesigner):
        label = "MyLocation"
        n_locations = 5

    creator.create(
        n_agents=10,
        df=df,
        location_designers=[MyLocationDesigner],
        clear=False,
    )

    assert len(model.agents) == 10
    assert len(model.locations) == 5

    creator.create(
        n_agents=10,
        df=df,
        location_designers=[MyLocationDesigner],
        clear=False,
    )

    assert len(model.agents) == 20
    assert len(model.locations) == 10

    creator.create(
        n_agents=10,
        df=df,
        location_designers=[MyLocationDesigner],
        clear=True,
    )

    assert len(model.agents) == 10
    assert len(model.locations) == 5
