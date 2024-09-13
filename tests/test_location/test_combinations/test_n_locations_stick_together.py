# %%
import pandas as pd

import popy

# %%


def test_1():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil"], "class_id": [1, 2, 1, 2]})

    class Classroom(popy.MagicLocation):
        n_locations = 4

        def stick_together(self, agent):
            return agent.class_id

    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[Classroom])

    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=df.columns, node_color="class_id")

    for location in model.locations[0:3]:
        print(location)
        print(location.agents)

    assert len(model.agents) == 4
    assert len(model.locations) == 4

    for location in model.locations[0:2]:
        assert len(location.agents) == 2

    for agent in model.agents:
        assert agent.neighbors(location_classes=[Classroom])[0].class_id == agent.class_id
    assert all(not location.agents for location in model.locations[2:])


test_1()

# %%
# TODO was macht hier noch Sinn zu testen
