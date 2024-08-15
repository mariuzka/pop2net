# %%
import pandas as pd
import popy


def test_1():
    df = pd.DataFrame({"status": ["pupil", "pupil", "pupil", "pupil"], "class_id": [1, 2, 1, 2]})

    class Classroom(popy.MagicLocation):
        n_agents = 2

        def stick_together(self, agent):
            return agent.class_id

    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[Classroom])

    assert len(model.agents) == 4
    assert len(model.locations) == 2

    for location in model.locations:
        assert len(location.agents) == 2

    for agent in model.agents:
        assert agent.neighbors(location_classes=[Classroom])[0].class_id == agent.class_id

    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=df.columns, node_color="class_id")


# stick together with uneven agent-location "seats"
def test_2():
    df = pd.DataFrame(
        {"status": ["pupil", "pupil", "pupil", "pupil", "pupil"], "class_id": [1, 2, 1, 2, 1]}
    )

    class Classroom(popy.MagicLocation):
        n_agents = 2

        def stick_together(self, agent):
            return agent.class_id

    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[Classroom])
    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=df.columns, node_color="class_id")

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

    class Classroom(popy.MagicLocation):
        n_agents = 2

        def split(self, agent):
            return agent.class_id

        def stick_together(self, agent):
            return agent.friends

    model = popy.Model()
    creator = popy.Creator(model=model)
    creator.create(df=df, location_classes=[Classroom])
    inspector = popy.NetworkInspector(model)
    inspector.plot_bipartite_network()
    inspector.plot_agent_network(node_attrs=df.columns, node_color="class_id")

    assert len(model.agents) == 6
    assert len(model.locations) == 4

    expected_loc_lens = [1, 1, 2, 2]
    for location in model.locations:
        assert len(location.agents) in expected_loc_lens
        del expected_loc_lens[expected_loc_lens.index(len(location.agents))]

    for agent in model.agents:
        assert all(nghbr.class_id == agent.class_id for nghbr in agent.neighbors())


test_3()

# %%


def test_4():
    # A test with many stick_together-values

    model = popy.Model()
    creator = popy.Creator(model=model)

    df = pd.DataFrame(
        {"group": [1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 3, 2, 3, 4, 5, 6, 6, 6, 6, 6, 10, 23, 10, 1, 1, 1]}
    )

    # location without stick_together()
    class TestLocation(popy.MagicLocation):
        n_locations = 5

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 5
    assert len(model.agents) == 26

    # assert that not all members of a group are in the same location
    assert not all(
        agent_i.TestLocation == agent_j.TestLocation
        for agent_i in model.agents
        for agent_j in model.agents
        if agent_i.group == agent_j.group
    )

    model = popy.Model()
    creator = popy.Creator(model=model)

    # location with stick_together()
    class TestLocation(popy.MagicLocation):
        n_locations = 5

        def stick_together(self, agent):
            return agent.group

    creator.create_agents(df=df)
    creator.create_locations(location_classes=[TestLocation])

    assert len(model.locations) == 5
    assert len(model.agents) == 26

    # assert that all members of a group are in the same location
    assert all(
        agent_i.TestLocation == agent_j.TestLocation
        for agent_i in model.agents
        for agent_j in model.agents
        if agent_i.group == agent_j.group
    )
