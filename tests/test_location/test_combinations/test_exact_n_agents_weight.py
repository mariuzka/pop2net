# %%
import pandas as pd

import pop2net as p2n

# %%


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "B"],
        },
    )

    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.MagicLocation):
        n_agents = 2
        only_exact_n_agents = True

        def weight(self, agent):
            return 1

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 1
    assert len(model.agents) == 3
    assert len(model.locations[0].agents) == 2
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert all(model.locations[0].get_weight(agent) == 1 for agent in model.locations[0].agents)


test_1()
