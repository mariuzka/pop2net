# %%
import pandas as pd

import popy


# %%
def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "B", "B", "A", "A", "A", "B", "B", "B", "A", "B", "A", "B"],
        },
    )

    class TestLocation1(popy.MagicLocation):
        overcrowding = None
        n_agents = 5

        def split(self, agent):
            return agent.status

    class TestLocation2(popy.MagicLocation):
        overcrowding = True
        n_agents = 5

        def split(self, agent):
            return agent.status

    class TestLocation3(popy.MagicLocation):
        overcrowding = False
        n_agents = 5

        def split(self, agent):
            return agent.status

    model = popy.Model()
    creator = popy.Creator(model)
    creator.create(df=df, location_classes=[TestLocation1])
    assert len(model.agents) == 14
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 7
    assert len(model.locations[1].agents) == 7
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert all(agent.status == "B" for agent in model.locations[1].agents)

    model = popy.Model()
    creator = popy.Creator(model)
    creator.create(df=df, location_classes=[TestLocation2])
    assert len(model.agents) == 14
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 7
    assert len(model.locations[1].agents) == 7
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert all(agent.status == "B" for agent in model.locations[1].agents)

    model = popy.Model()
    creator = popy.Creator(model)
    creator.create(df=df, location_classes=[TestLocation3])
    assert len(model.agents) == 14
    assert len(model.locations) == 4
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 5
    assert len(model.locations[3].agents) == 2
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert all(agent.status == "A" for agent in model.locations[1].agents)
    assert all(agent.status == "B" for agent in model.locations[2].agents)
    assert all(agent.status == "B" for agent in model.locations[3].agents)


test_1()
# %%
