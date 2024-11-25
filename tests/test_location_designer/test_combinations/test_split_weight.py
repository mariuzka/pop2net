import pandas as pd

import pop2net as p2n


def test_1():
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    df = pd.DataFrame({"status": ["A", "B", "B", "A", "A"]})

    class ClassRoom(p2n.LocationDesigner):
        def split(self, agent):
            return agent.status

        def weight(self, agent):
            return 5

    creator.create_agents(df=df)
    creator.create_locations(location_designers=[ClassRoom])

    assert len(model.locations) == 2
    assert len(model.agents) == 5
    assert len(model.locations[0].agents) == 3
    assert len(model.locations[1].agents) == 2
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert all(agent.status == "B" for agent in model.locations[1].agents)

    #
    locations_weights = []
    # model sum weight
    for location in model.locations:
        locations_weights.append(
            sum([model.get_weight(agent, location) for agent in location.agents])
        )
    assert sum(locations_weights) == 25
    # individual weights
    assert all(location.get_weight(agent) == 5 for agent in location.agents)


def test_2():
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    df = pd.DataFrame(
        {
            "status": ["A", "B", "A", "B", "A"],
        }
    )

    class ClassRoom(p2n.LocationDesigner):
        def split(self, agent):
            return agent.status

        def weight(self, agent):
            if agent.status == "A":
                return 2
            if agent.status == "B":
                return 4

    creator.create_agents(df=df)
    creator.create_locations(location_designers=[ClassRoom])

    assert len(model.locations) == 2
    assert len(model.agents) == 5
    assert len(model.locations[0].agents) == 3
    assert len(model.locations[1].agents) == 2
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert all(agent.status == "B" for agent in model.locations[1].agents)

    assert (
        sum([model.get_weight(agent, model.locations[0]) for agent in model.locations[0].agents])
        == 6
    )
    assert (
        sum([model.get_weight(agent, model.locations[1]) for agent in model.locations[1].agents])
        == 8
    )
    assert all(model.locations[0].get_weight(agent) == 2 for agent in model.locations[0].agents)
    assert all(model.locations[1].get_weight(agent) == 4 for agent in model.locations[1].agents)


def test_3():
    model = p2n.Model()
    creator = p2n.Creator(model=model)
    df = pd.DataFrame({"status": ["A", "B", "A", "B"], "attention_span": [1, 3, 2.5, 4]})

    class ClassRoom(p2n.LocationDesigner):
        def split(self, agent):
            return agent.status

        def weight(self, agent):
            return agent.attention_span

    creator.create_agents(df=df)
    creator.create_locations(location_designers=[ClassRoom])

    assert len(model.locations) == 2
    assert len(model.agents) == 4
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert all(agent.status == "B" for agent in model.locations[1].agents)

    assert (
        sum([model.get_weight(agent, model.locations[0]) for agent in model.locations[0].agents])
        == 3.5
    )

    assert (
        sum([model.get_weight(agent, model.locations[1]) for agent in model.locations[1].agents])
        == 7
    )
