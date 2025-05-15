import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil"],
        }
    )

    class School(p2n.LocationDesigner):
        n_locations = 1

    class Classroom(p2n.LocationDesigner):
        n_locations = 2

        def nest(self):
            return School

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[School, Classroom])
    inspector = p2n.NetworkInspector(env)
    inspector.plot_bipartite_network()

    assert len(env.actors) == 4
    assert len(env.locations) == 3

    for location in env.locations:
        if location.type == "School":
            assert len(location.actors) == 4
        if location.type == "Classroom":
            assert len(location.actors) == 2

    for actor in env.actors:
        assert actor.neighbors(location_labels=["Classroom"])[0] in actor.neighbors(
            location_labels=["School"]
        )


# TODO
# n_locations wird ignoriert, wenn das obere Level von nest 2 instanzen hat
# und das untere nur 1, es werden trotzdem 2 Classrooms erstellt
def test_2():
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil"],
        }
    )

    class School(p2n.LocationDesigner):
        n_locations = 2

    class Classroom(p2n.LocationDesigner):
        n_locations = 1

        def nest(self):
            return School

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[School, Classroom])
    inspector = p2n.NetworkInspector(env)
    inspector.plot_bipartite_network()
    print(len(env.locations))

    assert len(env.actors) == 4

    # TODO
    # assert len(env.locations) == 3

    for location in env.locations:
        if location.type == "School":
            assert len(location.actors) == 2
        if location.type == "Classroom":
            pass
            # TODO
            # assert len(location.actors) == 4
