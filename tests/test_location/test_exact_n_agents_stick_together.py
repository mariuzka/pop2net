# %%

import pandas as pd

import popy


# %%
def test_1():
    df = pd.DataFrame(
        {"status": ["pupil", "pupil", "pupil", "pupil", "pupil"], "class_id": [1, 2, 1, 2, 1]}
    )

    class Classroom(popy.MagicLocation):
        n_agents = 2
        only_exact_n_agents = False

        def stick_together(self, agent):
            return agent.class_id

    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[Classroom])

    assert len(model.agents) == 5
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 3

    for agent in model.agents:
        assert agent.neighbors(location_classes=[Classroom])[0].class_id == agent.class_id

    # with exact agent set to True
    class Classroom(popy.MagicLocation):
        n_agents = 2
        only_exact_n_agents = True

        def stick_together(self, agent):
            return agent.class_id

    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[Classroom])

    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=df.columns, node_color="class_id")

    assert len(model.agents) == 5
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 2

    for agent in model.agents:
        if agent.locations:
            assert agent.neighbors(location_classes=[Classroom])[0].class_id == agent.class_id
    assert all(not agent.locations for agent in model.agents if agent.class_id == 1)


test_1()
# %%
