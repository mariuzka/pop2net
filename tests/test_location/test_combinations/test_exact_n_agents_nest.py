# %%
import pandas as pd

import popy

# %%


def test_1():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil", "pupil"]})
    model = popy.Model()
    creator = popy.Creator(model=model)

    class Classroom(popy.MagicLocation):
        n_agents = 3
        only_exact_n_agents = False

        def nest(self):
            return School

    class School(popy.MagicLocation):
        pass

    creator.create(df=df, location_classes=[Classroom, School])

    assert len(model.agents) == 5
    assert len(model.locations) == 3
    assert len(model.locations[0].agents) == 3
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 5

    # Version with set to true
    model = popy.Model()
    creator = popy.Creator(model=model)

    class Classroom(popy.MagicLocation):
        n_agents = 3
        only_exact_n_agents = True

        def nest(self):
            return School

    class School(popy.MagicLocation):
        pass

    creator.create(df=df, location_classes=[Classroom, School])
    inspector = popy.NetworkInspector(model=model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=["status"])

    assert len(model.agents) == 5
    assert len(model.locations) == 2
    assert len(model.locations[0].agents) == 3
    assert len(model.locations[1].agents) == 5


test_1()


# %%
def test_2():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil", "pupil", "pupil"]})
    model = popy.Model()
    creator = popy.Creator(model=model)

    class Classroom(popy.MagicLocation):
        n_agents = 2
        only_exact_n_agents = True

        def nest(self):
            return School

    class School(popy.MagicLocation):
        n_agents = 4
        only_exact_n_agents = True

    creator.create(df=df, location_classes=[Classroom, School])
    inspector = popy.NetworkInspector(model=model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=["status", "id"])

    assert len(model.agents) == 6
    assert len(model.locations) == 4
    assert len(model.locations[0].agents) == 2
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 2
    assert len(model.locations[3].agents) == 4
    assert model.locations[2].agents not in model.locations[3].agents


test_2()
