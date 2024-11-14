import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A", "B", "B", "B", "B", "A", "A"],
        },
    )

    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
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


# %%


def test_2():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A"],
            "sex": ["m", "m", "m", "w"],
        },
    )

    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 1

        def split(self, agent):
            return [agent.status, agent.sex]

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])

    inspector = p2n.NetworkInspector(model=model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=["status", "sex"])
    assert len(model.locations) == 8
    assert len(model.agents) == 4
    assert len(model.locations[0].agents) == 1
    assert len(model.locations[1].agents) == 1
    assert len(model.locations[2].agents) == 1
    assert len(model.locations[3].agents) == 1
    assert len(model.locations[4].agents) == 1
    assert len(model.locations[5].agents) == 1
    assert len(model.locations[6].agents) == 1
    assert len(model.locations[7].agents) == 1


# %%


def test_3():
    df = pd.DataFrame(
        {
            "status": ["A", "B", "B", "A"],
            "sex": ["m", "m", "m", "w"],
        },
    )

    model = p2n.Model()
    creator = p2n.Creator(model)

    class TestLocation(p2n.LocationDesigner):
        n_agents = 1

        def split(self, agent):
            return str(agent.status) + str(agent.sex)

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])

    inspector = p2n.NetworkInspector(model=model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=["status", "sex"])
    assert len(model.locations) == 4
    assert len(model.agents) == 4
    assert len(model.locations[0].agents) == 1
    assert len(model.locations[1].agents) == 1
    assert len(model.locations[2].agents) == 1
    assert len(model.locations[3].agents) == 1


# %%
