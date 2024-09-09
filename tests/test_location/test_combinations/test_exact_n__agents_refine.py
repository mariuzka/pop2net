# %%
import pandas as pd

import popy


# %%
def test_1():
    df = pd.DataFrame(
        {
            "status": ["A","A","A", "B","B"],
        },
    )

    class TestLocation(popy.MagicLocation):
        n_agents = 2
        only_exact_n_agents = True

        def refine(self):
            if len(self.agents) % 3 != 0:
                new_agent = popy.Agent(model)
                new_agent.status = "C"
                self.add_agent(new_agent)
            
    model = popy.Model()
    creator = popy.Creator(model)
    creator.create(df=df, location_classes=[TestLocation])

    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=df.columns, node_color="status")

    assert len(model.agents) == 7
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 3
    assert len(model.locations[1].agents) == 3
    assert sum(not agent.locations for agent in model.agents) == 1
    assert sum(agent.status == "A" for agent in model.locations[0].agents) == 2
    assert sum(agent.status == "C" for agent in model.locations[0].agents) == 1
    assert sum(agent.status == "A" for agent in model.locations[1].agents) == 1
    assert sum(agent.status == "B" for agent in model.locations[1].agents) == 1
    assert sum(agent.status == "C" for agent in model.locations[1].agents) == 1

test_1()
# %%
