# %%
import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "A", "B"],
        }
    )
    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class TestLocation(p2n.LocationDesigner):
        only_exact_n_agents = False
        n_agents = 2

        def filter(self, agent):
            return agent.status == "A"

    creator.create(df=df, location_designers=[TestLocation])

    assert len(model.agents) == 4
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 2
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert len(model.locations[1].agents) == 1
    assert all(agent.status == "A" for agent in model.locations[1].agents)
    assert all(not agent.locations for agent in model.agents if agent.status == "B")

    model = p2n.Model()
    creator = p2n.Creator(model=model)

    class TestLocation(p2n.LocationDesigner):
        only_exact_n_agents = True
        n_agents = 2

        def filter(self, agent):
            return agent.status == "A"

    creator.create(df=df, location_designers=[TestLocation])

    assert len(model.agents) == 4
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 2
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert all(not agent.locations for agent in model.agents if agent.status == "B")
