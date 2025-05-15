import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["teacher", "teacher", "pupil", "pupil", "pupil"],
        },
    )

    class Teacher(p2n.MeltLocationDesigner):
        n_actors = 1

        def filter(self, actor):
            return actor.status == "teacher"

    class Pupils(p2n.MeltLocationDesigner):
        n_actors = 1

        def filter(self, actor):
            return actor.status == "pupil"

    class Classroom(p2n.LocationDesigner):
        def melt(self):
            return Teacher, Pupils

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create_actors(df=df)
    creator.create_locations(location_designers=[Classroom])

    assert len(env.actors) == 5
    assert len(env.locations) == 3

    for location in env.locations:
        assert location.actors[0].status == "teacher"
        assert location.actors[1].status == "pupil"


def test_2():
    df = pd.DataFrame(
        {
            "status": ["teacher", "teacher", "pupil", "pupil", "pupil"],
        },
    )

    class Teacher(p2n.MeltLocationDesigner):
        n_actors = 1

        def filter(self, actor):
            return actor.status == "teacher"

    class Pupils(p2n.MeltLocationDesigner):
        n_actors = 2

        def filter(self, actor):
            return actor.status == "pupil"

    class Classroom(p2n.LocationDesigner):
        n_actors = 2

        def melt(self):
            return Teacher, Pupils

    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    creator.create_actors(df=df)
    creator.create_locations(location_designers=[Classroom])

    assert len(env.actors) == 5
    assert len(env.locations) == 2

    for location in env.locations:
        assert location.actors[0].status == "teacher"
        assert location.actors[1].status == "pupil"
