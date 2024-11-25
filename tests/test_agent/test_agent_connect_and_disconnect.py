import pop2net as p2n


def test_agent_connect_1():
    model = p2n.Model()
    agent1 = p2n.Agent(model)
    agent2 = p2n.Agent(model)
    agent3 = p2n.Agent(model)

    class Home(p2n.Location):
        pass

    class School(p2n.Location):
        pass

    agent1.connect(
        agent=agent2,
        location_cls=Home,
    )

    agent2.connect(
        agent=agent3,
        location_cls=School,
    )

    assert len(model.agents) == 3

    assert isinstance(model.locations[0], Home)
    assert isinstance(model.locations[1], School)

    assert agent1 in model.locations[0].agents
    assert agent1 not in model.locations[1].agents

    assert agent2 in model.locations[0].agents
    assert agent2 in model.locations[1].agents

    assert agent3 not in model.locations[0].agents
    assert agent3 in model.locations[1].agents

    agent1.disconnect(
        agent2,
        location_labels=None,
        remove_locations=False,
        remove_neighbor=True,
        remove_self=True,
    )


def test_agent_disconnect_1():
    model = p2n.Model()
    agent1 = p2n.Agent(model)
    agent2 = p2n.Agent(model)
    agent3 = p2n.Agent(model)

    class Home(p2n.Location):
        pass

    class School(p2n.Location):
        pass

    agent1.connect(
        agent=agent2,
        location_cls=Home,
    )

    agent2.connect(
        agent=agent3,
        location_cls=School,
    )

    agent1.disconnect(
        agent2,
        location_labels=None,
        remove_locations=False,
        remove_neighbor=True,
        remove_self=True,
    )

    assert len(model.agents) == 3

    assert isinstance(model.locations[0], Home)
    assert isinstance(model.locations[1], School)

    assert agent1 not in model.locations[0].agents
    assert agent1 not in model.locations[1].agents

    assert agent2 not in model.locations[0].agents
    assert agent2 in model.locations[1].agents

    assert agent3 not in model.locations[0].agents
    assert agent3 in model.locations[1].agents

    agent2.disconnect(
        agent3,
        location_labels=None,
        remove_locations=False,
        remove_neighbor=True,
        remove_self=False,
    )

    assert len(model.agents) == 3

    assert isinstance(model.locations[0], Home)
    assert isinstance(model.locations[1], School)

    assert agent1 not in model.locations[0].agents
    assert agent1 not in model.locations[1].agents

    assert agent2 not in model.locations[0].agents
    assert agent2 in model.locations[1].agents

    assert agent3 not in model.locations[0].agents
    assert agent3 not in model.locations[1].agents


def test_agent_disconnect_2():
    model = p2n.Model()
    agent1 = p2n.Agent(model)
    agent2 = p2n.Agent(model)
    agent3 = p2n.Agent(model)

    class Home(p2n.Location):
        pass

    class School(p2n.Location):
        pass

    agent1.connect(
        agent=agent2,
        location_cls=Home,
    )

    agent1.connect(
        agent=agent2,
        location_cls=School,
    )

    agent1.disconnect(
        agent2,
        location_labels=["Home"],
        remove_locations=True,
        remove_neighbor=True,
        remove_self=True,
    )

    assert len(model.agents) == 3

    assert isinstance(model.locations[0], School)

    assert agent1 in model.locations[0].agents

    assert agent2 in model.locations[0].agents

    assert agent3 not in model.locations[0].agents

    agent1.disconnect(
        agent2,
        location_labels=["School"],
        remove_locations=False,
        remove_neighbor=False,
        remove_self=True,
    )

    assert len(model.agents) == 3

    assert isinstance(model.locations[0], School)

    assert agent1 not in model.locations[0].agents

    assert agent2 in model.locations[0].agents

    assert agent3 not in model.locations[0].agents
