from collections import Counter

import pandas as pd

import pop2net as p2n


# %%
# TODO Falsde False, False True und True True durchgehen pro Test, dass sollte dann auch reichen?
def test_1():
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil", "pupil", "pupil", "pupil"],
        }
    )

    class School(p2n.LocationDesigner):
        overcrowding = False
        n_agents = 5

    class Classroom(p2n.LocationDesigner):
        overcrowding = False
        n_agents = 5

        def nest(self):
            return School

    model = p2n.Model()
    creator = p2n.Creator(model=model)
    creator.create(df=df, location_classes=[School, Classroom])
    inspector = p2n.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=df)

    assert len(model.agents) == 7
    assert len(model.locations) == 4
    assert len(model.locations[0].agents) == 5
    assert len(model.locations[1].agents) == 2
    assert len(model.locations[2].agents) == 5
    assert len(model.locations[3].agents) == 2


# %%
# TODO das von oben nur mit True True und eine Variante wo True False jeweils gemischt ist


def test_2():
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil", "pupil", "pupil", "pupil", "pupil"],
            "group": [1, 2, 1, 2, 1, 2, 1, 2],
            "_id": [1, 2, 3, 4, 5, 6, 7, 8],
        }
    )

    class School(p2n.LocationDesigner):
        n_agents = 4

    class Classroom(p2n.LocationDesigner):
        n_agents = 2

        def split(self, agent):
            return agent.group

    model = p2n.Model()
    creator = p2n.Creator(model=model)
    creator.create(
        df=df,
        location_classes=[School, Classroom],
        delete_magic_agent_attributes=False,
    )

    assert len(model.agents) == 8
    assert len(model.locations) == 6

    for location in model.locations:
        if location.type == "School":
            assert len(location.agents) == 4
            counter = Counter([agent.group for agent in location.agents])
            assert counter[1] == 2
            assert counter[2] == 2

    assert not all(
        location.agents[0].School == location.agents[1].School
        for location in model.locations
        if location.type == "Classroom"
    )

    inspector = p2n.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=df.columns, agent_color="id")

    class School(p2n.LocationDesigner):
        n_agents = 4

    class Classroom(p2n.LocationDesigner):
        n_agents = 2

        def split(self, agent):
            return agent.group

        def nest(self):
            return School

    model = p2n.Model()
    creator = p2n.Creator(model=model)
    creator.create(
        df=df,
        location_classes=[School, Classroom],
        delete_magic_agent_attributes=False,
    )

    assert len(model.agents) == 8
    assert len(model.locations) == 6
    assert all(
        location.agents[0].School == location.agents[1].School
        for location in model.locations
        if location.type == "Classroom"
    )

    inspector = p2n.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=df.columns, agent_color="group")

    for location in model.locations:
        if location.type == "School":
            assert len(location.agents) == 4
        if location.type == "Classroom":
            assert len(location.agents) == 2

    for location in model.locations:
        if location.type == "School":
            assert len(location.agents) == 4
            counter = Counter([agent.group for agent in location.agents])
            assert counter[1] == 2
            assert counter[2] == 2

    assert any(
        agent.neighbors(location_classes=[Classroom])
        not in agent.neighbors(location_classes=[School])
        for agent in model.agents
    )

    for location in model.locations:
        if location.type == "School":
            for agent in location.agents:
                assert all(agent.School == nghbr.School for nghbr in agent.neighbors())


def test_3():
    class City(p2n.LocationDesigner):
        n_agents = 4

    class Group(p2n.LocationDesigner):
        n_agents = 2

        def split(self, agent):
            return agent.group

    model = p2n.Model()
    creator = p2n.Creator(model=model)

    for i in range(8):
        agent = p2n.Agent(model=model)
        agent.group = i % 2

    creator.create_locations(
        location_classes=[City, Group],
        delete_magic_agent_attributes=False,
    )

    for location in model.locations.select(model.locations.type == "City"):
        assert int(location.agents[0].group) == 0
        assert int(location.agents[1].group) == 1
        assert int(location.agents[2].group) == 0
        assert int(location.agents[3].group) == 1

    for location in model.locations.select(model.locations.type == "Group"):
        assert location.agents[0].group == location.agents[1].group

    # not all members of the same group are also in the same city (which is not desired)
    assert not all(
        location.agents[0].City == location.agents[1].City for location in model.locations
    )

    class GroupNestedInCity(Group):
        def nest(self):
            return City

    model = p2n.Model()
    creator = p2n.Creator(model=model)
    creator.create_locations(
        location_classes=[City, GroupNestedInCity],
        delete_magic_agent_attributes=False,
    )

    for location in model.locations.select(model.locations.type == "City"):
        assert int(location.agents[0].group) == 0
        assert int(location.agents[1].group) == 1
        assert int(location.agents[2].group) == 0
        assert int(location.agents[3].group) == 1

    for location in model.locations.select(model.locations.type == "Group"):
        assert location.agents[0].group == location.agents[1].group

    # all members of a group are in the same city
    assert all(location.agents[0].City == location.agents[1].City for location in model.locations)
