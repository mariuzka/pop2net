# %%
import pandas as pd

import popy

from collections import Counter


# %%

def test_1():

    model = popy.Model()
    creator = popy.Creator(model=model)
    inspector = popy.NetworkInspector(model=model)
    df = pd.DataFrame(
        {"friend_group": [1, 1, 1, 1, 2,2,2, 2, 3, 3, 3,3,4,4],
         "split_group": [1,2,1,2,1,2,1,2,1,2,1,2,1,2]
         }
    )
    class TestLocation(popy.MagicLocation):
        n_agents = 4

        def split(self, agent):
            return agent.split_group
        def stick_together(self, agent):
            return agent.friend_group
        
    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])

    inspector.plot_agent_network(node_attrs=["friend_group"])

    for i, location in enumerate(model.locations):
        print(f"Location;{i}")
        [print(agent.friend_group) for agent in location.agents]

    assert len(model.locations) == 4
    assert len(model.agents) == 14
    # assert expecetd locations split and agent distribution
    for i, location in enumerate(model.locations):
        match i:
            case 0:
                assert len(location.agents) == 4
                counter = Counter([agent.friend_group for agent in location.agents])
                assert list(counter.keys()) == [1,2]
                assert list(counter.values()) == [2,2]
            case 1:
                assert len(location.agents) == 3
                counter = Counter([agent.friend_group for agent in location.agents])
                assert list(counter.keys()) == [3,4]
                assert list(counter.values()) == [2,1]
            case 2:
                assert len(location.agents) == 4
                counter = Counter([agent.friend_group for agent in location.agents])
                assert list(counter.keys()) == [1,2]
                assert list(counter.values()) == [2,2]
            case 3:
                assert len(location.agents) == 3
                counter = Counter([agent.friend_group for agent in location.agents])
                assert list(counter.keys()) == [3,4]
                assert list(counter.values()) == [2,1]
test_1()