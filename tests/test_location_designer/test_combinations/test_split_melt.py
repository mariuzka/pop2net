import pandas as pd

import pop2net as p2n


def test_1():
    model = p2n.Model()
    creator = p2n.Creator(model=model)
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
        def filter(self, agent):
            return agent.status == "pupil"

        def split(self, agent):
            return agent.class_id

    class TeacherHelper(p2n.LocationDesigner):
        def filter(self, agent):
            return agent.status == "teacher"

        def split(self, agent):
            return agent.class_id

    class ClassRoom(p2n.LocationDesigner):
        def melt(self):
            return PupilHelper, TeacherHelper

    creator.create_agents(df=df)
    creator.create_locations(location_designers=[ClassRoom])

    assert len(model.agents) == 9
    assert len(model.locations) == 3

    for location in model.locations:
        assert len(location.agents) == 3
        assert all(location.agents[0].class_id == agent.class_id for agent in location.agents)


def test_2():
    model = p2n.Model()
    creator = p2n.Creator(model=model)
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
        def filter(self, agent):
            return agent.status == "pupil"

        def split(self, agent):
            return agent.class_id

    class TeacherHelper(p2n.MeltLocationDesigner):
        def filter(self, agent):
            return agent.status == "teacher"

        def split(self, agent):
            return agent.class_id

    class ClassRoom(p2n.LocationDesigner):
        def melt(self):
            return PupilHelper, TeacherHelper

    class SchoolHelper(p2n.MeltLocationDesigner):
        def filter(self, agent):
            return agent.status == "principal"

    class School(p2n.LocationDesigner):
        def melt(self):
            return ClassRoom, SchoolHelper

    creator.create_agents(df=df)
    creator.create_locations(location_designers=[ClassRoom, School])

    assert len(model.agents) == 10
    assert len(model.locations) == 4

    for location in model.locations:
        if location.label == "ClassRoom":
            assert len(location.agents) == 3
            assert all(location.agents[0].class_id == agent.class_id for agent in location.agents)
        else:
            assert len(location.agents) == 10
