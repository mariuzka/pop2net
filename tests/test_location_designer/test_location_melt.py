import pandas as pd

import pop2net as p2n

df = pd.DataFrame(
    {
        "status": ["teacher", "teacher", "pupil", "pupil", "pupil"],
    },
)


def test_recycle_1():
    class Teacher(p2n.MeltLocationDesigner):
        label = "Teacher"
        n_actors = 1

        def filter(self, actor):
            return actor.status == "teacher"

    class Pupils(p2n.MeltLocationDesigner):
        label = "Pupil"
        n_actors = 1

        def filter(self, actor):
            return actor.status == "pupil"

    class Classroom(p2n.LocationDesigner):
        label = "Classroom"
        recycle = True

        def melt(self):
            return Teacher, Pupils

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create_actors(df=df)
    creator.create_locations(location_designers=[Classroom])
    inspector = p2n.NetworkInspector(env)
    inspector.plot_bipartite_network()

    assert len(env.actors) == 5
    assert len(env.locations) == 3

    for location in env.locations:
        assert location.actors[0].status == "teacher"
        assert location.actors[1].status == "pupil"


def test_recycle_2():
    class Teacher(p2n.MeltLocationDesigner):
        n_actors = 1

        def filter(self, actor):
            return actor.status == "teacher"

    class Pupils(p2n.MeltLocationDesigner):
        n_actors = 1

        def filter(self, actor):
            return actor.status == "pupil"

    class Classroom(p2n.LocationDesigner):
        recycle = False

        def melt(self):
            return Teacher, Pupils

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create_actors(df=df)
    creator.create_locations(location_designers=[Classroom])
    inspector = p2n.NetworkInspector(env)
    inspector.plot_bipartite_network()

    assert len(env.actors) == 5
    assert len(env.locations) == 2

    for location in env.locations:
        assert location.actors[0].status == "teacher"
        assert location.actors[1].status == "pupil"

    assert env.actors[4].status == "pupil"
    assert len(env.actors[4].locations) == 0
