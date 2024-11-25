from collections import Counter

import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil"],
        }
    )

    class SchoolDesigner(p2n.LocationDesigner):
        label = "School"
        n_agents = 2

    class ClassroomDesigner(p2n.LocationDesigner):
        label = "Classroom"
        n_agents = 2

        def nest(self):
            return "School"

    model = p2n.Model()
    creator = p2n.Creator(model=model)
    creator.create(df=df, location_designers=[SchoolDesigner, ClassroomDesigner])

    assert len(model.agents) == 4
    assert len(model.locations) == 4

    for location in model.locations:
        if location.label == "School":
            assert len(location.agents) == 2
        if location.label == "Classroom":
            assert len(location.agents) == 2

    for agent in model.agents:
        assert (
            agent.neighbors(location_labels=["Classroom"])[0]
            is agent.neighbors(location_labels=["School"])[0]
        )


def test_2():
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil", "pupil", "pupil", "pupil", "pupil"],
            "group": [1, 2, 1, 2, 1, 2, 1, 2],
            "_id": [1, 2, 3, 4, 5, 6, 7, 8],
        }
    )

    class SchoolDesigner(p2n.LocationDesigner):
        label = "School"
        n_agents = 4

    class ClassroomDesigner(p2n.LocationDesigner):
        label = "Classroom"
        n_agents = 2

        def split(self, agent):
            return agent.group

    model = p2n.Model()
    creator = p2n.Creator(model=model)
    creator.create(
        df=df,
        location_designers=[SchoolDesigner, ClassroomDesigner],
        delete_magic_agent_attributes=False,
    )

    assert len(model.agents) == 8
    assert len(model.locations) == 6

    for location in model.locations:
        if location.label == "School":
            assert len(location.agents) == 4
            counter = Counter([agent.group for agent in location.agents])
            assert counter[1] == 2
            assert counter[2] == 2

    assert not all(
        location.agents[0].School == location.agents[1].School
        for location in model.locations
        if location.label == "Classroom"
    )

    class SchoolDesigner(p2n.LocationDesigner):
        label = "School"
        n_agents = 4

    class ClassroomDesigner(p2n.LocationDesigner):
        label = "Classroom"
        n_agents = 2

        def split(self, agent):
            return agent.group

        def nest(self):
            return "School"

    model = p2n.Model()
    creator = p2n.Creator(model=model)
    creator.create(
        df=df,
        location_designers=[SchoolDesigner, ClassroomDesigner],
        delete_magic_agent_attributes=False,
    )

    assert len(model.agents) == 8
    assert len(model.locations) == 6
    assert all(
        location.agents[0].School == location.agents[1].School
        for location in model.locations
        if location.label == "Classroom"
    )

    for location in model.locations:
        if location.label == "School":
            assert len(location.agents) == 4
        if location.label == "Classroom":
            assert len(location.agents) == 2

    for location in model.locations:
        if location.label == "School":
            assert len(location.agents) == 4
            counter = Counter([agent.group for agent in location.agents])
            assert counter[1] == 2
            assert counter[2] == 2

    assert any(
        agent.neighbors(location_labels=["Classroom"])
        not in agent.neighbors(location_labels=["School"])
        for agent in model.agents
    )

    for location in model.locations:
        if location.label == "School":
            for agent in location.agents:
                assert all(agent.School == nghbr.School for nghbr in agent.neighbors())