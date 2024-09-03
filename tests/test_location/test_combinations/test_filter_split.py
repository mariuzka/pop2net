# %%
import pandas as pd

import popy
from popy.creator import Creator


# %%
def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B"],
            "sex": ["w", "m", "m", "m", "w"],
        },
    )

    model = popy.Model()
    creator = Creator(model)

    class TestLocationA(popy.MagicLocation):
        def filter(self, agent):
            return agent.status == "A"
        def split(self, agent):
            return agent.sex

    class TestLocationB(popy.MagicLocation):
        def filter(self, agent):
            return agent.status == "B" 
        def split(self, agent):
            return agent.sex

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocationA, TestLocationB])
    assert len(model.locations) == 4
    assert len(model.agents) == 5

    for location in model.locations:
        if location.type == "TestLocationA":
            assert all(agent.status == "A" for agent in location.agents)
        if location.type == "TestLocationB":
            assert all(agent.status == "B" for agent in location.agents)
    
    assert len(model.locations[0].agents) == 1
    assert len(model.locations[1].agents) == 1
    assert len(model.locations[2].agents) == 2
    assert len(model.locations[3].agents) == 1
    assert model.locations[0].agents[0].sex == "w"
    assert model.locations[1].agents[0].sex == "m"
    assert all(agent.sex == "m" for agent in model.locations[2].agents)
    assert all(agent.sex == "w" for agent in model.locations[3].agents)

test_1()
    

# %%
