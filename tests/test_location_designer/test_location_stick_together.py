import pandas as pd

import pop2net as p2n


def test_1():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil"], "class_id": [1, 2, 1, 2]})

    class Classroom(p2n.LocationDesigner):
        n_agents = 2

        def stick_together(self, agent):
            return agent.class_id

    model = p2n.Model()
    creator = p2n.Creator(model=model)
    creator.create(df=df, location_designers=[Classroom])

    assert len(model.agents) == 4
    assert len(model.locations) == 2

    for location in model.locations:
        assert len(location.agents) == 2

    for agent in model.agents:
        assert agent.neighbors(location_labels=["Classroom"])[0].class_id == agent.class_id

    inspector = p2n.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=df.columns, agent_color="class_id")


# stick together with uneven agent-location "seats"
def test_2():
    df = pd.DataFrame(
        {"status": ["pupil", "pupil", "pupil", "pupil", "pupil"], "class_id": [1, 2, 1, 2, 1]}
    )

    class Classroom(p2n.LocationDesigner):
        n_agents = 2

        def stick_together(self, agent):
            return agent.class_id

    model = p2n.Model()
    creator = p2n.Creator(model=model)
    creator.create(df=df, location_designers=[Classroom])
    inspector = p2n.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=df.columns, agent_color="class_id")

    assert len(model.agents) == 5
    assert len(model.locations) == 2

    expected_loc_lens = [2, 3]
    for location in model.locations:
        assert len(location.agents) in expected_loc_lens
        del expected_loc_lens[expected_loc_lens.index(len(location.agents))]

    for agent in model.agents:
        assert all(nghbr.class_id == agent.class_id for nghbr in agent.neighbors())


# stick_together with split
def test_3():
    df = pd.DataFrame(
        {
            "status": ["pupil", "pupil", "pupil", "pupil", "pupil", "pupil"],
            "class_id": [1, 1, 1, 2, 2, 2],
            "friends": [1, 2, 1, 2, 1, 2],
        }
    )

    class Classroom(p2n.LocationDesigner):
        n_agents = 2

        def split(self, agent):
            return agent.class_id

        def stick_together(self, agent):
            return agent.friends

    model = p2n.Model()
    creator = p2n.Creator(model=model)
    creator.create(df=df, location_designers=[Classroom])
    inspector = p2n.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(agent_attrs=df.columns, agent_color="class_id")

    assert len(model.agents) == 6
    assert len(model.locations) == 4

    expected_loc_lens = [1, 1, 2, 2]
    for location in model.locations:
        assert len(location.agents) in expected_loc_lens
        del expected_loc_lens[expected_loc_lens.index(len(location.agents))]

    for agent in model.agents:
        assert all(nghbr.class_id == agent.class_id for nghbr in agent.neighbors())


def test_4():
    # A test with many stick_together-values

    model = p2n.Model()
    creator = p2n.Creator(model=model)

    df = pd.DataFrame(
        {"group": [1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 3, 2, 3, 4, 5, 6, 6, 6, 6, 6, 10, 23, 10, 1, 1, 1]}
    )

    # location without stick_together()
    class TestLocation(p2n.LocationDesigner):
        n_locations = 5

    creator.create_agents(df=df)
    creator.create_locations(
        location_designers=[TestLocation],
        delete_magic_agent_attributes=False,
    )

    assert len(model.locations) == 5
    assert len(model.agents) == 26

    # assert that not all members of a group are in the same location
    assert not all(
        agent_i.TestLocation == agent_j.TestLocation
        for agent_i in model.agents
        for agent_j in model.agents
        if agent_i.group == agent_j.group
    )

    model = p2n.Model()
    creator = p2n.Creator(model=model)
    inspector = p2n.NetworkInspector(model=model)

    # location with stick_together()
    class TestLocation(p2n.LocationDesigner):
        n_locations = 5

        def stick_together(self, agent):
            return agent.group

    creator.create_agents(df=df)
    creator.create_locations(
        location_designers=[TestLocation],
        delete_magic_agent_attributes=False,
    )

    assert len(model.locations) == 5
    assert len(model.agents) == 26

    # assert that all members of a group are in the same location
    assert all(
        agent_i.TestLocation == agent_j.TestLocation
        for agent_i in model.agents
        for agent_j in model.agents
        if agent_i.group == agent_j.group
    )

    inspector.plot_agent_network(agent_attrs=["group"])
