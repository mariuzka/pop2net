# %%

import pandas as pd

import popy


# %%
def test_1():
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil"],
        }
    )

    class School(popy.MagicLocation):
        n_locations = 1

    class Classroom(popy.MagicLocation):
        n_locations = 2

        def nest(self):
            return School

    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[School, Classroom])
    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()

    assert len(model.agents) == 4
    assert len(model.locations) == 3

    for location in model.locations:
        if location.type == "School":
            assert len(location.agents) == 4
        if location.type == "Classroom":
            assert len(location.agents) == 2

    for agent in model.agents:
        assert agent.neighbors(location_classes=[Classroom])[0] in agent.neighbors(
            location_classes=[School]
        )


test_1()


# %%
# TODO
# n_locations wird ignoriert, wenn das obere Level von nest 2 instanzen hat
# und das untere nur 1, es werden trotzdem 2 Classrooms erstellt
def test_2():
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil"],
        }
    )

    class School(popy.MagicLocation):
        n_locations = 2

    class Classroom(popy.MagicLocation):
        n_locations = 1

        def nest(self):
            return School

    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[School, Classroom])
    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()
    print(len(model.locations))

    assert len(model.agents) == 4
    assert len(model.locations) == 3

    for location in model.locations:
        if location.type == "School":
            assert len(location.agents) == 2
        if location.type == "Classroom":
            assert len(location.agents) == 4


test_2()
# %%
