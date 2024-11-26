import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B"],
        },
    )

    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        def weight(self, agent):
            return 1

    creator.create_agents(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 1
    assert len(model.agents) == 5
    assert len(model.locations[0].agents) == 5
    # sum of weights correct?
    assert (
        sum([model.get_weight(agent, model.locations[0]) for agent in model.locations[0].agents])
        == 5
    )
    # inidividual weights correct?
    assert all(
        model.get_weight(agent, model.locations[0]) == 1 for agent in model.locations[0].agents
    )


def test_2():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B"],
        },
    )

    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        def weight(self, agent):
            if agent.status == "A":
                return 1
            if agent.status == "B":
                return 5

    creator.create_agents(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 1
    assert len(model.agents) == 5
    assert len(model.locations[0].agents) == 5
    # sum of weights correct?
    assert (
        sum([model.get_weight(agent, model.locations[0]) for agent in model.locations[0].agents])
        == 17
    )
    # inidividual weights correct?
    assert all(
        model.get_weight(agent, model.locations[0]) == 1
        if agent.status == "A"
        else model.get_weight(agent, model.locations[0]) == 5
        for agent in model.locations[0].agents
    )


def test_3():
    df = pd.DataFrame(
        {
            "status": [1, 5, 5, 1, 5],
        },
    )

    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        def weight(self, agent):
            return agent.status

    creator.create_agents(df=df)
    creator.create_locations(location_designers=[TestLocation])

    assert len(model.locations) == 1
    assert len(model.agents) == 5
    assert len(model.locations[0].agents) == 5
    # sum of weights correct?
    assert (
        sum([model.get_weight(agent, model.locations[0]) for agent in model.locations[0].agents])
        == 17
    )
    # inidividual weights correct?
    assert all(
        model.get_weight(agent, model.locations[0]) == 1
        if agent.status == 1
        else model.get_weight(agent, model.locations[0]) == 5
        for agent in model.locations[0].agents
    )
