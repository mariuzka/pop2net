# %%

import pandas as pd

import pop2net as p2n


# %%
# TODO ohne n_agents oder n_locations seh ich keine Möglichkeit stick_together mitr filter sinnvoll zu testen
def test_1():
    model = p2n.Model()
    creator = p2n.Creator(model=model)
    df = pd.DataFrame(
        {"friend_group": [1, 2, 2, 3, 1, 3, 2], "filter_group": [1, 1, 2, 2, 1, 1, 2]}
    )

    class TestLocationA(p2n.MagicLocation):
        n_agents = 2

        def filter(self, agent):
            return agent.filter_group == 1

        def stick_together(self, agent):
            return agent.friend_group

    class TestLocationB(p2n.MagicLocation):
        n_agents = 2

        def filter(self, agent):
            return agent.filter_group == 2

        def stick_together(self, agent):
            return agent.friend_group

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocationA, TestLocationB])
    inspector = p2n.NetworkInspector(model=model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=["friend_group", "filter_group"])

    assert len(model.locations) == 4
    assert len(model.agents) == 7
    assert len([location for location in model.locations if location.type == "TestLocationA"]) == 2
    assert len([location for location in model.locations if location.type == "TestLocationB"]) == 2

    assert len(model.locations[0].agents) == 2
    assert all(agent.friend_group == 1 for agent in model.locations[0].agents)
    assert len(model.locations[1].agents) == 2
    assert all(agent.friend_group in [2, 3] for agent in model.locations[1].agents)
    assert len(model.locations[2].agents) == 2
    assert all(agent.friend_group == 2 for agent in model.locations[2].agents)
    assert len(model.locations[3].agents) == 1
    assert all(agent.friend_group == 3 for agent in model.locations[3].agents)


test_1()
# %%
