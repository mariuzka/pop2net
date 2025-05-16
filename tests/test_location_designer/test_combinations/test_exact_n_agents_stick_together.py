import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {"status": ["pupil", "pupil", "pupil", "pupil", "pupil"], "class_id": [1, 2, 1, 2, 1]}
    )

    class Classroom(p2n.LocationDesigner):
        n_actors = 2
        only_exact_n_actors = False

        def stick_together(self, actor):
            return actor.class_id

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[Classroom])

    assert len(env.actors) == 5
    assert len(env.locations) == 2
    assert len(env.locations[0].actors) == 2
    assert len(env.locations[1].actors) == 3

    for actor in env.actors:
        assert actor.neighbors(location_labels=["Classroom"])[0].class_id == actor.class_id

    # with exact actor set to True
    class Classroom(p2n.LocationDesigner):
        n_actors = 2
        only_exact_n_actors = True

        def stick_together(self, actor):
            return actor.class_id

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create(df=df, location_designers=[Classroom])

    inspector = p2n.NetworkInspector(env)
    inspector.plot_bipartite_network()
    inspector.plot_actor_network(actor_attrs=df.columns, actor_color="class_id")

    assert len(env.actors) == 5
    assert len(env.locations) == 1
    assert len(env.locations[0].actors) == 2

    for actor in env.actors:
        if actor.locations:
            assert actor.neighbors(location_labels=["Classroom"])[0].class_id == actor.class_id
    assert all(not actor.locations for actor in env.actors if actor.class_id == 1)
