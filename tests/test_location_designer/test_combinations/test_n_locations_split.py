import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "C"],
        },
    )

    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_locations = None

        def split(self, agent):
            return agent.status

    creator.create_agents(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.agents) == 6
    assert TestLocation.n_locations is None


def test_2():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "C"],
        },
    )

    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_locations = 3

        def split(self, agent):
            return agent.status

    creator.create_agents(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.agents) == 6

    # check if the n_locations attribute is overwritten with None
    assert TestLocation.n_locations is None
