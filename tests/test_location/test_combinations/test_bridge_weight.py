import pop2net as p2n


def test_1():
    # recycle=False+weight
    model = p2n.Model()
    creator = p2n.Creator(model)


    for _ in range(3):
        agent = p2n.Agent(model)
        agent.gender = "w"


    for _ in range(2):
        agent = p2n.Agent(model)
        agent.gender = "m"

    class Partnership(p2n.MagicLocation):
        recycle = False

        def bridge(self, agent):
            return agent.gender
        

        def weight(self, agent):
            return 1



    creator.create_locations(location_classes=[Partnership])

    assert len(model.locations) == 2
    assert len(model.agents) == 5

    for location in model.locations:
        assert len(location.agents) == 2
        assert [agent.gender for agent in location.agents].count("m") == 1
        assert [agent.gender for agent in location.agents].count("w") == 1
        assert [agent.get_location_weight(location) for agent in location.agents].count(1) == 2
        assert all(agent.get_location_weight(location) == 1 for agent in location.agents)

    assert len(model.agents[0].locations) == 1
    assert len(model.agents[1].locations) == 1
    assert len(model.agents[2].locations) == 0
    assert len(model.agents[3].locations) == 1
    assert len(model.agents[4].locations) == 1


def test_2():
    # recyle=True+weight
    model = p2n.Model()
    creator = p2n.Creator(model)


    for _ in range(3):
        agent = p2n.Agent(model)
        agent.gender = "w"


    for _ in range(2):
        agent = p2n.Agent(model)
        agent.gender = "m"

    class Partnership(p2n.MagicLocation):
        recycle = True

        def bridge(self, agent):
            return agent.gender
        

        def weight(self, agent):
            return 1

    creator.create_locations(location_classes=[Partnership])

    assert len(model.locations) == 3
    assert len(model.agents) == 5

    for location in model.locations:
        assert len(location.agents) == 2
        assert [agent.gender for agent in location.agents].count("m") == 1
        assert [agent.gender for agent in location.agents].count("w") == 1
        assert [agent.get_location_weight(location) for agent in location.agents].count(1) == 2
        assert all(agent.get_location_weight(location) == 1 for agent in location.agents)

    assert sum(
        [model.agents[3].get_location_weight(location) for location in model.agents[3].locations]
        ) == 2
    assert len(model.agents[0].locations) == 1
    assert len(model.agents[1].locations) == 1
    assert len(model.agents[2].locations) == 1
    assert len(model.agents[3].locations) == 2
    assert len(model.agents[4].locations) == 1