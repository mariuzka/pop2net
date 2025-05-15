import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": [
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
            ],
            "class_id": [1, 2, 1, 2, 1, 2, 1, 2, 3],
        }
    )
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class Classroom1(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.class_id == 1

        def nest(self):
            return School

    class Classroom2(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.class_id == 2

        def nest(self):
            return School

    class School(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.class_id == 1 or actor.class_id == 2

    creator.create(df=df, location_designers=[Classroom1, Classroom2, School])

    assert len(env.actors) == 9
    assert len(env.locations) == 3
    assert all(actor.class_id == 1 for actor in env.locations[0].actors)
    assert all(actor.class_id == 2 for actor in env.locations[1].actors)
    assert all(actor.class_id in [1, 2] for actor in env.locations[2].actors)
    assert all(not actor.locations for actor in env.actors if actor.class_id == 3)


def test_2():
    df = pd.DataFrame(
        {
            "status": [
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
                "pupil",
            ],
            "school_id": [1, 2, 1, 2, 1, 2, 1, 2, 3],
        }
    )
    env = p2n.Environment()
    creator = p2n.Creator(env=env)

    class Classroom1(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.school_id == 1

        def nest(self):
            return School1

    class Classroom2(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.school_id == 2

        def nest(self):
            return School2

    class School1(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.school_id == 1

    class School2(p2n.LocationDesigner):
        def filter(self, actor):
            return actor.school_id == 2

    creator.create(df=df, location_designers=[Classroom1, Classroom2, School1, School2])

    assert len(env.actors) == 9
    assert len(env.locations) == 4
    assert all(actor.school_id == 1 for actor in env.locations[0].actors)
    assert all(actor.school_id == 2 for actor in env.locations[1].actors)
    assert all(actor.school_id == 1 for actor in env.locations[2].actors)
    assert all(actor.school_id == 2 for actor in env.locations[3].actors)
    assert all(not actor.locations for actor in env.actors if actor.school_id == 3)
