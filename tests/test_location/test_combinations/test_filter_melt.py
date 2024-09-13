# %%
import pandas as pd

import popy


# %%
def test_1():
    model = popy.Model()
    creator = popy.Creator(model=model)
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil", "teacher"],
        }
    )

    class PupilHelper(popy.MagicLocation):
        def filter(self, agent):
            return agent.status == "pupil"

    class TeacherHelper(popy.MagicLocation):
        def filter(self, agent):
            return agent.status == "teacher"

    class ClassRoom(popy.MagicLocation):
        def melt(self):
            return PupilHelper, TeacherHelper

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[ClassRoom])

    assert len(model.agents) == 5
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 5
    assert sum(agent.status == "pupil" for agent in model.locations[0].agents) == 4


test_1()


# %%
def test_2():
    model = popy.Model()
    creator = popy.Creator(model=model)
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil", "teacher", "teacher"],
            "classroom_id": [1, 1, 2, 2, 1, 2],
        }
    )

    class PupilHelper(popy.MagicLocation):
        def filter(self, agent):
            return agent.status == "pupil"

    class TeacherHelper(popy.MagicLocation):
        def filter(self, agent):
            return agent.status == "teacher"

    class ClassRoom(popy.MagicLocation):
        def filter(self, agent):
            return agent.classroom_id == 1

        def melt(self):
            return PupilHelper, TeacherHelper

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[ClassRoom])

    assert len(model.agents) == 6
    assert len(model.locations) == 1
    assert len(model.locations[0].agents) == 3
    assert sum(agent.status == "pupil" for agent in model.locations[0].agents) == 2
    assert sum(agent.status == "teacher" for agent in model.locations[0].agents) == 1
    assert sum(not agent.locations for agent in model.agents) == 3


test_2()
# %%
