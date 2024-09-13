# %%
import pandas as pd

import pop2net as p2n


# %%
def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "C"],
        },
    )

    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.MagicLocation):
        n_agents = 2

        def weight(self, agent):
            return 1

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.agents) == 6
    for location in model.locations:
        assert len(location.agents) == 2
        assert sum([location.get_weight(agent) for agent in location.agents]) == 2
        assert all(location.get_weight(agent) == 1 for agent in location.agents)


test_1()


# %%
def test_2():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "C"],
        },
    )

    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.MagicLocation):
        n_agents = 2

        def weight(self, agent):
            if agent.status == "A":
                return 1
            if agent.status == "B":
                return 2
            if agent.status == "C":
                return 3

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 3
    assert len(model.agents) == 6
    sum_of_sum = 0
    for location in model.locations:
        sum_of_sum += sum([location.get_weight(agent) for agent in location.agents])
        assert len(location.agents) == 2
    assert sum_of_sum == 11
    for agent in model.agents:
        if agent.status == "A":
            assert agent.get_location_weight(agent.locations[0]) == 1
        if agent.status == "B":
            assert agent.get_location_weight(agent.locations[0]) == 2
        if agent.status == "C":
            assert agent.get_location_weight(agent.locations[0]) == 3


test_2()


# %%
