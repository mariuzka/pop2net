import popy
import pandas as pd

df = pd.DataFrame(
    {
        "status": ["teacher", "teacher", "pupil", "pupil", "pupil"],
    },
)


def test_recycle_1():
    class Teacher(popy.MeltLocation):
        n_agents = 1

        def filter(self, agent):
            return agent.status == "teacher"

    class Pupils(popy.MeltLocation):
        n_agents = 1

        def filter(self, agent):
            return agent.status == "pupil"

    class Classroom(popy.MagicLocation):
        recycle = True

        def melt(self):
            return Teacher, Pupils

    model = popy.Model()
    creator = popy.Creator(model)
    creator.create_agents(df=df)
    creator.create_locations(location_classes=[Classroom])
    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()

    assert len(model.agents) == 5
    assert len(model.locations) == 3

    for location in model.locations:
        assert location.agents[0].status == "teacher"
        assert location.agents[1].status == "pupil"


def test_recycle_2():
    class Teacher(popy.MeltLocation):
        n_agents = 1

        def filter(self, agent):
            return agent.status == "teacher"

    class Pupils(popy.MeltLocation):
        n_agents = 1

        def filter(self, agent):
            return agent.status == "pupil"

    class Classroom(popy.MagicLocation):
        recycle = False

        def melt(self):
            return Teacher, Pupils

    model = popy.Model()
    creator = popy.Creator(model)
    creator.create_agents(df=df)
    creator.create_locations(location_classes=[Classroom])
    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()

    assert len(model.agents) == 5
    assert len(model.locations) == 2

    for location in model.locations:
        assert location.agents[0].status == "teacher"
        assert location.agents[1].status == "pupil"

    assert model.agents[4].status == "pupil"
    assert len(model.agents[4].locations) == 0
