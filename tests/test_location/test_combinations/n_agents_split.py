# %%
from collections import Counter

import pandas as pd

import popy


# %%
def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "B", "B", "B", "A", "A"],
        },
    )

    model = popy.Model()
    creator = popy.Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 2

        def split(self, agent):
            return agent.status

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 5
    assert len(model.agents) == 10
    for location in model.locations:
        if location.agents[0].status == "A":
            assert len(location.agents) == 2
            assert all(agent.status == "A" for agent in location.agents)
        if location.agents[0].status == "B":
            assert len(location.agents) == 2
            assert all(agent.status == "B" for agent in location.agents)

test_1()
# %%
# TODO Hier stimmt aus meiner Sicht etwas nicht - Unexpected Verhalten
# Ich hätte 4 Locations erwartet, 1 pro mögliche Attributskombination
# also A/m, A/w, B/m, B/w und dann wegen n_agents zusätzlich 1 Location
# da B/m doppelt vorkommt
# Ich bekomme aber 8 Locations und Agenten werden doppelt zugewiesen (siehe print)

def test_2():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A"],
            "sex": ["m", "m", "m", "w"],
        },
    )

    model = popy.Model()
    creator = popy.Creator(model)

    class TestLocation(popy.MagicLocation):
        n_agents = 1
        def split(self, agent):
            return [agent.status, agent.sex]

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])

    inspector = popy.NetworkInspector(model=model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=["status", "sex"])
    #assert len(model.locations) == 8
    assert len(model.agents) == 4
    assert len(model.locations[0].agents) == 1
    assert len(model.locations[1].agents) == 1
    assert len(model.locations[2].agents) == 1
    assert len(model.locations[3].agents) == 1
    print(model.locations[4:9])
    for location in model.locations:
        for agent in location.agents:
            print(agent.status)
            print(agent.sex)
            print("/n")
    
test_2()
# %%
