# %%
import pandas as pd

import popy


# %%
def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "A", "B"],
        }
    )
    model = popy.Model()
    creator = popy.Creator(model=model)

    class TestLocation(popy.MagicLocation):
        only_exact_n_agents = False
        n_agents = 2

        def filter(self, agent):
            return agent.status == "A"

    creator.create(df=df, location_classes=[TestLocation])
    inspector = popy.NetworkInspector(model=model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=["status"])

    assert len(model.agents) == 4
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 2
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert len(model.locations[1].agents) == 1
    assert all(agent.status == "A" for agent in model.locations[1].agents)
    assert all(not agent.locations for agent in model.agents if agent.status == "B")

    model = popy.Model()
    creator = popy.Creator(model=model)

    class TestLocation(popy.MagicLocation):
        only_exact_n_agents = True
        n_agents = 2

        def filter(self, agent):
            return agent.status == "A"

    creator.create(df=df, location_classes=[TestLocation])
    inspector = popy.NetworkInspector(model=model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=["status"])

    assert len(model.agents) == 4
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 2
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert all(not agent.locations for agent in model.agents if agent.status == "B")


test_1()
# %%
