# Hier muss man die Hierarchie berücksichtgigen und testen exact size only überschreibt das Verhalten von overcrrowd
# %%
import pandas as pd

import popy


# %%
def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "A", "A", "A", "A", "A"],
        },
    )

    class TestLocation(popy.MagicLocation):
        overcrowding = None
        n_agents = 5
        only_exact_n_agents = False

    class TestLocation2(popy.MagicLocation):
        overcrowding = True
        n_agents = 5
        only_exact_n_agents = False

    class TestLocation3(popy.MagicLocation):
        overcrowding = False
        n_agents = 5
        only_exact_n_agents = False

    model = popy.Model()
    creator = popy.Creator(model)
    creator.create(df=df, location_classes=[TestLocation])
    inspector = popy.NetworkInspector(model)
    inspector.plot_agent_network(node_attrs=df.columns, node_color="status")
    assert len(model.agents) == 7
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 7

    model = popy.Model()
    creator = popy.Creator(model)
    creator.create(df=df, location_classes=[TestLocation2])
    inspector = popy.NetworkInspector(model)
    inspector.plot_agent_network(node_attrs=df.columns, node_color="status")
    assert len(model.agents) == 7
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 7

    model = popy.Model()
    creator = popy.Creator(model)
    creator.create(df=df, location_classes=[TestLocation3])
    inspector = popy.NetworkInspector(model)
    inspector.plot_agent_network(node_attrs=df.columns, node_color="status")
    assert len(model.agents) == 7
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 2


test_1()


# %%
# %%
def test_1():
    df = pd.DataFrame(
        {
            "status": ["A", "A", "A", "A", "A", "A", "A"],
        },
    )

    class TestLocation(popy.MagicLocation):
        overcrowding = None
        n_agents = 5
        only_exact_n_agents = True

    class TestLocation2(popy.MagicLocation):
        overcrowding = True
        n_agents = 5
        only_exact_n_agents = True

    class TestLocation3(popy.MagicLocation):
        overcrowding = False
        n_agents = 5
        only_exact_n_agents = True

    model = popy.Model()
    creator = popy.Creator(model)
    creator.create(df=df, location_classes=[TestLocation])
    inspector = popy.NetworkInspector(model)
    inspector.plot_agent_network(node_attrs=df.columns, node_color="status")
    assert len(model.agents) == 7
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 5
    assert sum(not agent.locations for agent in model.agents) == 2

    model = popy.Model()
    creator = popy.Creator(model)
    creator.create(df=df, location_classes=[TestLocation2])
    inspector = popy.NetworkInspector(model)
    inspector.plot_agent_network(node_attrs=df.columns, node_color="status")
    assert len(model.agents) == 7
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 5
    assert sum(not agent.locations for agent in model.agents) == 2

    model = popy.Model()
    creator = popy.Creator(model)
    creator.create(df=df, location_classes=[TestLocation3])
    inspector = popy.NetworkInspector(model)
    inspector.plot_agent_network(node_attrs=df.columns, node_color="status")
    assert len(model.agents) == 7
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 5
    assert sum(not agent.locations for agent in model.agents) == 2


test_1()
# %%
