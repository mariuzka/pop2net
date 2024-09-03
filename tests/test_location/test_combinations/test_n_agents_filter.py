# %%
import pandas as pd

import popy
from popy.creator import Creator


# %%
def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "A", "B"],
        },
    )

    model = popy.Model()
    creator = Creator(model)

    class TestLocationA(popy.MagicLocation):
        n_agents = 2
        def filter(self, agent):
            return agent.status == "A"

    class TestLocationB(popy.MagicLocation):
        n_agents = 2
        def filter(self, agent):
            return agent.status == "B"

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocationA, TestLocationB])

    assert len(model.locations) == 4
    assert len(model.agents) == 7
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 1
    assert len(model.locations[2].agents) == 2
    assert len(model.locations[3].agents) == 2
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert all(agent.status == "A" for agent in model.locations[1].agents)
    assert all(agent.status == "B" for agent in model.locations[2].agents)
    assert all(agent.status == "B" for agent in model.locations[3].agents)

test_1()
# %%
