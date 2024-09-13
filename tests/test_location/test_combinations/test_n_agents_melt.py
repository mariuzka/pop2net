# %%
import pandas as pd

import pop2net as p2n

# %%


def test_1():
    df = pd.DataFrame(
        {
            "status": ["teacher", "teacher", "pupil", "pupil", "pupil"],
        },
    )

    class Teacher(p2n.MeltLocation):
        n_agents = 1

        def filter(self, agent):
            return agent.status == "teacher"

    class Pupils(p2n.MeltLocation):
        n_agents = 1

        def filter(self, agent):
            return agent.status == "pupil"

    class Classroom(p2n.MagicLocation):
        def melt(self):
            return Teacher, Pupils

    model = p2n.Model()
    creator = p2n.Creator(model)
    creator.create_agents(df=df)
    creator.create_locations(location_classes=[Classroom])
    inspector = p2n.NetworkInspector(model)
    inspector.plot_bipartite_network()

    assert len(model.agents) == 5
    assert len(model.locations) == 3

    for location in model.locations:
        assert location.agents[0].status == "teacher"
        assert location.agents[1].status == "pupil"


test_1()


# %%
def test_2():
    df = pd.DataFrame(
        {
            "status": ["teacher", "teacher", "pupil", "pupil", "pupil"],
        },
    )

    class Teacher(p2n.MeltLocation):
        n_agents = 1

        def filter(self, agent):
            return agent.status == "teacher"

    class Pupils(p2n.MeltLocation):
        n_agents = 2

        def filter(self, agent):
            return agent.status == "pupil"

    class Classroom(p2n.MagicLocation):
        n_agents = 2

        def melt(self):
            return Teacher, Pupils

    model = p2n.Model()
    creator = p2n.Creator(model)
    creator.create_agents(df=df)
    creator.create_locations(location_classes=[Classroom])
    inspector = p2n.NetworkInspector(model)
    inspector.plot_bipartite_network()
    assert len(model.agents) == 5
    assert len(model.locations) == 2

    for location in model.locations:
        assert location.agents[0].status == "teacher"
        assert location.agents[1].status == "pupil"


test_2()
# %%
