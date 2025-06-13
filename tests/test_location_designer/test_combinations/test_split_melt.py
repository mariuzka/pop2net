import pandas as pd

import pop2net as p2n


def test_1():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    df = pd.DataFrame(
        {
            "status": [
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "teacher",
                "teacher",
                "teacher",
            ],
            "class_id": [1, 1, 2, 2, 3, 3, 1, 2, 3],
        }
    )

    class PupilHelper(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.status == "pupil"

        def split(self, actor):
            return actor.class_id

    class TeacherHelper(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.status == "teacher"

        def split(self, actor):
            return actor.class_id

    class ClassRoom(p2n.LocationDesigner):
        def melt(self):
            return PupilHelper, TeacherHelper

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[ClassRoom])

    assert len(env.actors) == 9
    assert len(env.locations) == 3

    for location in env.locations:
        assert len(location.actors) == 3
        assert all(location.actors[0].class_id == actor.class_id for actor in location.actors)


def test_2():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    df = pd.DataFrame(
        {
            "status": [
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "teacher",
                "teacher",
                "teacher",
                "principal",
            ],
            "class_id": [1, 1, 2, 2, 3, 3, 1, 2, 3, 0],
        }
    )

    class PupilHelper(p2n.MeltLocationDesigner):
        def filter(self, actor):
            return actor.status == "pupil"

        def split(self, actor):
            return actor.class_id

    class TeacherHelper(p2n.MeltLocationDesigner):
        def filter(self, actor):
            return actor.status == "teacher"

        def split(self, actor):
            return actor.class_id

    class ClassRoom(p2n.LocationDesigner):
        def melt(self):
            return PupilHelper, TeacherHelper

    class SchoolHelper(p2n.MeltLocationDesigner):
        def filter(self, actor):
            return actor.status == "principal"

    class School(p2n.LocationDesigner):
        def melt(self):
            return ClassRoom, SchoolHelper

    creator.create_actors(df=df)
    creator.create_locations(location_designers=[ClassRoom, School])

    assert len(env.actors) == 10
    assert len(env.locations) == 4

    for location in env.locations:
        if location.label == "ClassRoom":
            assert len(location.actors) == 3
            assert all(location.actors[0].class_id == actor.class_id for actor in location.actors)
        else:
            assert len(location.actors) == 10
