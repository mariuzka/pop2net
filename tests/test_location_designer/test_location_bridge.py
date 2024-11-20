import pop2net as p2n


def test_1():
    # basic test

    model = p2n.Model()
    creator = p2n.Creator(model)

    for _ in range(3):
        agent = p2n.Agent(model)
        agent.gender = "w"

    for _ in range(2):
        agent = p2n.Agent(model)
        agent.gender = "m"

    class HeteroRelationship(p2n.LocationDesigner):
        recycle = False

        def bridge(self, agent):
            return agent.gender

    creator.create_locations(location_designers=[HeteroRelationship])

    assert len(model.locations) == 2
    assert len(model.agents) == 5

    for location in model.locations:
        assert len(location.agents) == 2
        assert [agent.gender for agent in location.agents].count("m") == 1
        assert [agent.gender for agent in location.agents].count("w") == 1

    assert len(model.agents[0].locations) == 1
    assert len(model.agents[1].locations) == 1
    assert len(model.agents[2].locations) == 0
    assert len(model.agents[3].locations) == 1
    assert len(model.agents[4].locations) == 1


def test_2():
    # test n_locations

    model = p2n.Model()
    creator = p2n.Creator(model)

    for _ in range(3):
        agent = p2n.Agent(model)
        agent.gender = "w"

    for _ in range(2):
        agent = p2n.Agent(model)
        agent.gender = "m"

    class HeteroRelationship(p2n.LocationDesigner):
        recycle = False
        n_locations = 1

        def bridge(self, agent):
            return agent.gender

    creator.create_locations(location_designers=[HeteroRelationship])

    assert len(model.locations) == 1
    assert len(model.agents) == 5

    location = model.locations[0]
    assert len(location.agents) == 2
    assert [agent.gender for agent in location.agents].count("m") == 1
    assert [agent.gender for agent in location.agents].count("w") == 1

    assert len(model.agents[0].locations) == 1
    assert len(model.agents[1].locations) == 0
    assert len(model.agents[2].locations) == 0
    assert len(model.agents[3].locations) == 1
    assert len(model.agents[4].locations) == 0


def test_3():
    # test recycle

    model = p2n.Model()
    creator = p2n.Creator(model)

    for _ in range(3):
        agent = p2n.Agent(model)
        agent.gender = "w"

    for _ in range(2):
        agent = p2n.Agent(model)
        agent.gender = "m"

    class HeteroRelationship(p2n.LocationDesigner):
        recycle = True

        def bridge(self, agent):
            return agent.gender

    creator.create_locations(location_designers=[HeteroRelationship])

    assert len(model.locations) == 3
    assert len(model.agents) == 5

    for location in model.locations:
        assert len(location.agents) == 2
        assert [agent.gender for agent in location.agents].count("m") == 1
        assert [agent.gender for agent in location.agents].count("w") == 1

    assert len(model.agents[0].locations) == 1
    assert len(model.agents[1].locations) == 1
    assert len(model.agents[2].locations) == 1
    assert len(model.agents[3].locations) == 2
    assert len(model.agents[4].locations) == 1


def test_4():
    # test n_locations and recycle

    model = p2n.Model()
    creator = p2n.Creator(model)

    for _ in range(3):
        agent = p2n.Agent(model)
        agent.gender = "w"

    for _ in range(2):
        agent = p2n.Agent(model)
        agent.gender = "m"

    class HeteroRelationship(p2n.LocationDesigner):
        recycle = True
        n_locations = 1

        def bridge(self, agent):
            return agent.gender

    creator.create_locations(location_designers=[HeteroRelationship])

    assert len(model.locations) == 1
    assert len(model.agents) == 5

    location = model.locations[0]
    assert len(location.agents) == 2
    assert [agent.gender for agent in location.agents].count("m") == 1
    assert [agent.gender for agent in location.agents].count("w") == 1

    assert len(model.agents[0].locations) == 1
    assert len(model.agents[1].locations) == 0
    assert len(model.agents[2].locations) == 0
    assert len(model.agents[3].locations) == 1
    assert len(model.agents[4].locations) == 0
