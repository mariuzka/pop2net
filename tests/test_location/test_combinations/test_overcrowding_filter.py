import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "B", "B", "A", "A", "A", "B", "B", "B", "A", "B", "A", "B"],
        },
    )

    class TestLocationA1(p2n.MagicLocation):
        overcrowding = None
        n_agents = 5

        def filter(self, agent):
            return agent.status == "A"

    class TestLocationA2(p2n.MagicLocation):
        overcrowding = True
        n_agents = 5

        def filter(self, agent):
            return agent.status == "A"

    class TestLocationA3(p2n.MagicLocation):
        overcrowding = False
        n_agents = 5

        def filter(self, agent):
            return agent.status == "A"

    class TestLocationB1(p2n.MagicLocation):
        overcrowding = None
        n_agents = 5

        def filter(self, agent):
            return agent.status == "B"

    class TestLocationB2(p2n.MagicLocation):
        overcrowding = True
        n_agents = 5

        def filter(self, agent):
            return agent.status == "B"

    class TestLocationB3(p2n.MagicLocation):
        overcrowding = False
        n_agents = 5

        def filter(self, agent):
            return agent.status == "B"

    model = p2n.Model()
    creator = p2n.Creator(model)
    creator.create(df=df, location_classes=[TestLocationA1, TestLocationB1])
    assert len(model.agents) == 14
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 7
    assert len(model.locations[1].agents) == 7
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert all(agent.status == "B" for agent in model.locations[1].agents)

    model = p2n.Model()
    creator = p2n.Creator(model)
    creator.create(df=df, location_classes=[TestLocationA2, TestLocationB2])
    inspector = p2n.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=df.columns, agent_color="status")
    assert len(model.agents) == 14
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 7
    assert len(model.locations[1].agents) == 7
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert all(agent.status == "B" for agent in model.locations[1].agents)

    model = p2n.Model()
    creator = p2n.Creator(model)
    creator.create(df=df, location_classes=[TestLocationA3, TestLocationB3])
    inspector = p2n.NetworkInspector(model)
    inspector.plot_agent_network(agent_attrs=df.columns, agent_color="status")
    assert len(model.agents) == 14
    assert len(model.locations) == 4
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 5
    assert len(model.locations[3].agents) == 2
    assert all(agent.status == "A" for agent in model.locations[0].agents)
    assert all(agent.status == "A" for agent in model.locations[1].agents)
    assert all(agent.status == "B" for agent in model.locations[2].agents)
    assert all(agent.status == "B" for agent in model.locations[3].agents)
