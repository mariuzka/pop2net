# %%
import pandas as pd

import popy


# %%
def test_1():

    model = popy.Model()
    creator = popy.Creator(model=model)
    inspector = popy.NetworkInspector(model=model)
    df = pd.DataFrame(
        {"status": ["A", "B", "A", "B", "A"],
         })
    
    class ClassRoom(popy.MagicLocation):

        def filter(self, agent):
            return agent.status == "A"
        
        def weight(self, agent):
            if agent.status == "A":
                return 2
            else:
                return 1
                
    creator.create_agents(df=df)
    creator.create_locations(location_classes=[ClassRoom])
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=["status"])

    assert len(model.locations) == 1
    assert len(model.agents) == 5
    # TODO TypeError: attribute name must be string, not 'int' versteh das Problem nicht
    assert all(agent.get_location_weight(location = model.locations[0]) == 2 for agent in model.locations[0])
    
    assert len(model.locations[0].agents) == 3
    assert sum(not agent.locations for agent in model.agents) == 2

test_1()
# %%
