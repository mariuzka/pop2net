# %%
import pandas as pd

import popy

# %%
def test_1():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil"], "class_id": [1, 2, 1, 2]})

    class Classroom(popy.MagicLocation):
        n_agents = 2

        def stick_together(self, agent):
            return agent.class_id

    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[Classroom])

    assert len(model.agents) == 4
    assert len(model.locations) == 2

    for location in model.locations:
        assert len(location.agents) == 2

    for agent in model.agents:
        assert agent.neighbors(location_classes=[Classroom])[0].class_id == agent.class_id

    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=df.columns, node_color="class_id")

test_1()

# %%
# TODO Soll stick together Prio haben über n_agents? 
# Es werden nie vier Locations mit einem Agenten erzeugt
# mit der Config 
# overcrowding = False
# only_exact_n_agents = True
# wird KEINE Location erstellt
def test_2():
    df = pd.DataFrame(
        {"status": ["pupil", "pupil", "pupil", "pupil"], "class_id": [1,1,1,1]}
    )

    class Classroom(popy.MagicLocation):
        n_agents = 1
        #overcrowding = False
        #only_exact_n_agents = True
        def stick_together(self, agent):
            return agent.class_id

    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[Classroom])
    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=df.columns, node_color="status")
    print(len(model.locations))
    assert len(model.agents) == 4
    assert len(model.locations) == 4

test_2()
# %%
