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
        n_agents = 5
        only_exact_n_agents = False

    class TestLocation2(p2n.LocationDesigner):
        overcrowding = True
        n_agents = 5
        only_exact_n_agents = False

    class TestLocation3(p2n.LocationDesigner):
        overcrowding = False
        n_agents = 5
        only_exact_n_agents = False

    model = p2n.Model()
    creator = p2n.Creator(model)
    creator.create(df=df, location_designers=[TestLocation])

    assert len(model.agents) == 7
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 7

    model = p2n.Model()
    creator = p2n.Creator(model)
    creator.create(df=df, location_designers=[TestLocation2])

    assert len(model.agents) == 7
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 7

    model = p2n.Model()
    creator = p2n.Creator(model)
    creator.create(df=df, location_designers=[TestLocation3])

    assert len(model.agents) == 7
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 2


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "A", "A", "A", "A", "A"],
        },
    )

    class TestLocation(p2n.LocationDesigner):
        overcrowding = None
        n_agents = 5
        only_exact_n_agents = True

    class TestLocation2(p2n.LocationDesigner):
        overcrowding = True
        n_agents = 5
        only_exact_n_agents = True

    class TestLocation3(p2n.LocationDesigner):
        overcrowding = False
        n_agents = 5
        only_exact_n_agents = True

    model = p2n.Model()
    creator = p2n.Creator(model)
    creator.create(df=df, location_designers=[TestLocation])

    assert len(model.agents) == 7
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 5
    assert sum(not agent.locations for agent in model.agents) == 2

    model = p2n.Model()
    creator = p2n.Creator(model)
    creator.create(df=df, location_designers=[TestLocation2])

    assert len(model.agents) == 7
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 5
    assert sum(not agent.locations for agent in model.agents) == 2

    model = p2n.Model()
    creator = p2n.Creator(model)
    creator.create(df=df, location_designers=[TestLocation3])

    assert len(model.agents) == 7
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 5
    assert sum(not agent.locations for agent in model.agents) == 2
