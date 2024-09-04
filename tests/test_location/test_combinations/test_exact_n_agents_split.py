# %%
import pandas as pd

import popy
from popy.creator import Creator


# %%
def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "A", "B", "B", "B"],
        }
    )
    model = popy.Model()
    creator = popy.Creator(model=model)

    class TestLocation(popy.MagicLocation):
        only_exact_n_agents = False
        n_agents = 2
        def split(self,agent):
            return agent.status
        
    creator.create(df=df, location_classes=[TestLocation])
    inspector = popy.NetworkInspector(model = model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=["status"])

    assert len(model.agents) == 6
    assert len(model.locations) == 4
    assert len(model.locations[0].agents) == 2
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert len(model.locations[1].agents) == 1
    assert all(agent.status == "A" for agent in model.locations[1].agents)
    assert len(model.locations[2].agents) == 2
    assert all(agent.status == "B" for agent in model.locations[2].agents)
    assert len(model.locations[3].agents) == 1
    assert all(agent.status == "B" for agent in model.locations[3].agents)

    model = popy.Model()
    creator = popy.Creator(model=model)

    class TestLocation(popy.MagicLocation):
        only_exact_n_agents = True
        n_agents = 2
        def split(self,agent):
            return agent.status
        
    creator.create(df=df, location_classes=[TestLocation])
    inspector = popy.NetworkInspector(model = model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=["status"])

    assert len(model.agents) == 6
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 2
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert len(model.locations[1].agents) == 2
    assert all(agent.status == "B" for agent in model.locations[1].agents)
    assert sum(not agent.locations for agent in model.agents if agent.status == "B") == 1
    assert sum(not agent.locations for agent in model.agents if agent.status == "A") == 1
   

test_1()
# %%
