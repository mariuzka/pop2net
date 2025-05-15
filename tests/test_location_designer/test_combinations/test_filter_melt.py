import pandas as pd

import pop2net as p2n


def test_1():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil", "teacher"],
        }
    )

    class PupilHelper(p2n.MeltLocationDesigner):
        def filter(self, actor):
            return actor.status == "pupil"

    class TeacherHelper(p2n.MeltLocationDesigner):
        def filter(self, actor):
            return actor.status == "teacher"

    class ClassRoom(p2n.LocationDesigner):
        def melt(self):
            return PupilHelper, TeacherHelper

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[ClassRoom])

    assert len(env.actors) == 5
    assert len(env.locations) == 1
    assert len(env.locations[0].actors) == 5
    assert sum(actor.status == "pupil" for actor in env.locations[0].actors) == 4


def test_2():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil", "teacher", "teacher"],
            "classroom_id": [1, 1, 2, 2, 1, 2],
        }
    )

    class PupilHelper(p2n.MeltLocationDesigner):
        def filter(self, actor):
            return actor.status == "pupil"

    class TeacherHelper(p2n.MeltLocationDesigner):
        def filter(self, actor):
            return actor.status == "teacher"

    class ClassRoom(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.classroom_id == 1

        def melt(self):
            return PupilHelper, TeacherHelper

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[ClassRoom])

    assert len(env.actors) == 6
    assert len(env.locations) == 1
    assert len(env.locations[0].actors) == 3
    assert sum(actor.status == "pupil" for actor in env.locations[0].actors) == 2
    assert sum(actor.status == "teacher" for actor in env.locations[0].actors) == 1
    assert sum(not actor.locations for actor in env.actors) == 3
