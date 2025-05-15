import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil"], "class_id": [1, 2, 1, 2]})

    class Classroom(p2n.LocationDesigner):
        n_actors = 2

        def stick_together(self, actor):
            return actor.class_id

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[Classroom])

    assert len(env.actors) == 4
    assert len(env.locations) == 2

    for location in env.locations:
        assert len(location.actors) == 2

    for actor in env.actors:
        assert actor.neighbors(location_labels=["Classroom"])[0].class_id == actor.class_id

    inspector = p2n.NetworkInspector(env)
    inspector.plot_bipartite_network()
    inspector.plot_actor_network(actor_attrs=df.columns, actor_color="class_id")


def test_2():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil"], "class_id": [1, 1, 1, 1]})

    class Classroom(p2n.LocationDesigner):
        n_actors = 1

        def stick_together(self, actor):
            return actor.class_id

    env = p2n.Environment()

    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[Classroom])

    inspector = p2n.NetworkInspector(env)
    inspector.plot_bipartite_network()
    inspector.plot_actor_network(actor_attrs=df.columns, actor_color="status")

    assert len(env.actors) == 4
    assert len(env.locations) == 1


def test_3():
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil", "pupil", "pupil", "pupil"],
            "class_id": [1, 1, 1, 1, 2, 2, 3],
        }
    )

    class Classroom(p2n.LocationDesigner):
        n_actors = 1

        def stick_together(self, actor):
            return actor.class_id

    env = p2n.Environment()

    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[Classroom])

    inspector = p2n.NetworkInspector(env)
    inspector.plot_bipartite_network()
    inspector.plot_actor_network(actor_attrs=df.columns, actor_color="status")

    assert len(env.actors) == 7
    assert len(env.locations) == 3

    counter = 0
    for location in env.locations:
        if location.actors[0].class_id == 1:
            assert len(location.actors) == 4
            counter += 1

        if location.actors[0].class_id == 2:
            assert len(location.actors) == 2
            counter += 1

        if location.actors[0].class_id == 3:
            assert len(location.actors) == 1
            counter += 1

    assert counter == 3
