import pandas as pd

import pop2net as p2n
from pop2net.creator import Creator


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B"],
        },
    )

    model = p2n.Model()
    creator = Creator(model)

    class TestLocationA(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.status == "A"

    class TestLocationB(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.status == "B"

    creator.create_agents(df=df)
    creator.create_locations(location_designers=[TestLocationA, TestLocationB])

    assert len(model.locations) == 2
    assert len(model.agents) == 5
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 3
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert all(agent.status == "B" for agent in model.locations[1].agents)


def test_2():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B"],
            "sex": ["w", "m", "m", "m", "w"],
        },
    )

    model = p2n.Model()
    creator = Creator(model)

    class TestLocationA(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.status == "A" and agent.sex == "w"

    class TestLocationB(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.status == "B" and agent.sex == "w"

    creator.create_agents(df=df)
    creator.create_locations(location_designers=[TestLocationA, TestLocationB])

    assert len(model.locations) == 2
    assert len(model.agents) == 5
    assert len(model.locations[0].agents) == 1
    assert len(model.locations[1].agents) == 1
    assert all(agent.status == "A" and agent.sex == "w" for agent in model.locations[0].agents)
    assert all(agent.status == "B" and agent.sex == "w" for agent in model.locations[1].agents)
