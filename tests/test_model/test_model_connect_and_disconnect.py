import pop2net as p2n


def test_model_connect_agents_and_disconnect_agents_1():
    """A test without specifing locationt types and without removing locations from model."""

    model = p2n.Model()
    agent1 = p2n.Agent(model)
    agent2 = p2n.Agent(model)
    agent3 = p2n.Agent(model)
    agents = [agent1, agent2, agent3]

    class Home(p2n.Location):
        pass

    class School(p2n.Location):
        pass

    model.connect_agents(
        agents=agents,
        location_cls=Home,
    )

    model.connect_agents(
        agents=[agent1, agent2],
        location_cls=School,
    )

    assert len(model.agents) == 3

    assert isinstance(model.locations[0], Home)
    assert isinstance(model.locations[1], School)

    assert agent1 in model.locations[0].agents
    assert agent1 in model.locations[1].agents
    assert agent2 in model.locations[0].agents
    assert agent2 in model.locations[1].agents
    assert agent3 in model.locations[0].agents
    assert agent3 not in model.locations[1].agents

    model.disconnect_agents(agents, remove_locations=False)

    assert len(model.agents) == 3

    assert len(model.locations) == 2
    assert isinstance(model.locations[0], Home)
    assert isinstance(model.locations[1], School)

    assert len(model.locations[0].agents) == 0
    assert len(model.locations[1].agents) == 0

    assert len(agent1.locations) == 0
    assert len(agent2.locations) == 0
    assert len(agent3.locations) == 0


def test_model_connect_agents_and_disconnect_agents_2():
    """A test without removing locations from model."""

    model = p2n.Model()
    agent1 = p2n.Agent(model)
    agent2 = p2n.Agent(model)
    agent3 = p2n.Agent(model)
    agents = [agent1, agent2, agent3]

    class Home(p2n.Location):
        pass

    class School(p2n.Location):
        pass

    model.connect_agents(
        agents=agents,
        location_cls=Home,
    )

    model.connect_agents(
        agents=[agent1, agent2],
        location_cls=School,
    )

    model.disconnect_agents(agents, location_labels=[Home], remove_locations=False)

    assert len(model.agents) == 3

    assert len(model.locations) == 2
    assert isinstance(model.locations[0], Home)
    assert isinstance(model.locations[1], School)

    assert len(model.locations[0].agents) == 0
    assert len(model.locations[1].agents) == 2

    assert len(agent1.locations) == 1
    assert len(agent2.locations) == 1
    assert len(agent3.locations) == 0

    model.disconnect_agents(agents, location_labels=[School], remove_locations=False)

    assert len(model.agents) == 3

    assert len(model.locations) == 2
    assert isinstance(model.locations[0], Home)
    assert isinstance(model.locations[1], School)

    assert len(model.locations[0].agents) == 0
    assert len(model.locations[1].agents) == 0

    assert len(agent1.locations) == 0
    assert len(agent2.locations) == 0
    assert len(agent3.locations) == 0

    model.connect_agents(agents=agents, location_cls=School)
    model.disconnect_agents(agents=[agent1, agent2], location_labels=[School])

    assert len(model.agents) == 3

    assert len(model.locations) == 3
    assert isinstance(model.locations[0], Home)
    assert isinstance(model.locations[1], School)
    assert isinstance(model.locations[2], School)

    assert len(model.locations[0].agents) == 0
    assert len(model.locations[1].agents) == 0
    assert len(model.locations[2].agents) == 1

    assert len(agent1.locations) == 0
    assert len(agent2.locations) == 0
    assert len(agent3.locations) == 1


def test_model_connect_agents_and_disconnect_agents_3():
    model = p2n.Model()
    agent1 = p2n.Agent(model)
    agent2 = p2n.Agent(model)
    agent3 = p2n.Agent(model)
    agents = [agent1, agent2, agent3]

    class Home(p2n.Location):
        pass

    class School(p2n.Location):
        pass

    model.connect_agents(
        agents=agents,
        location_cls=Home,
    )

    model.connect_agents(
        agents=[agent1, agent2],
        location_cls=School,
    )

    model.disconnect_agents(agents, location_labels=[School], remove_locations=True)

    assert len(model.agents) == 3

    assert len(model.locations) == 1
    assert isinstance(model.locations[0], Home)

    assert len(model.locations[0].agents) == 3

    assert len(agent1.locations) == 1
    assert len(agent2.locations) == 1
    assert len(agent3.locations) == 1

    model.disconnect_agents(agents, location_labels=[Home], remove_locations=True)

    assert len(model.agents) == 3

    assert len(model.locations) == 0

    assert len(agent1.locations) == 0
    assert len(agent2.locations) == 0
    assert len(agent3.locations) == 0


def test_model_connect_agents_and_disconnect_agents_4():
    model = p2n.Model()
    agent1 = p2n.Agent(model)
    agent2 = p2n.Agent(model)
    agent3 = p2n.Agent(model)
    agents = [agent1, agent2, agent3]

    class Home(p2n.Location):
        pass

    class School(p2n.Location):
        pass

    model.connect_agents(
        agents=agents,
        location_cls=Home,
    )

    model.connect_agents(
        agents=[agent1, agent2],
        location_cls=School,
    )

    model.disconnect_agents(agents=[agent1, agent2], remove_locations=True)

    assert len(model.agents) == 3

    assert len(model.locations) == 0

    assert len(agent1.locations) == 0
    assert len(agent2.locations) == 0
    assert len(agent3.locations) == 0


def test_model_connect_agents_and_disconnect_agents_5():
    """Test agent.shared_locations()"""
    model = p2n.Model()
    agent1 = p2n.Agent(model)
    agent2 = p2n.Agent(model)

    class Home(p2n.Location):
        pass

    class School(p2n.Location):
        pass

    assert len(agent1.shared_locations(agent2)) == 0
    assert len(agent1.shared_locations(agent=agent2, location_labels=[Home])) == 0
    assert len(agent1.shared_locations(agent=agent2, location_labels=[School])) == 0

    model.connect_agents(
        agents=[agent1, agent2],
        location_cls=Home,
    )

    assert len(agent1.shared_locations(agent=agent2)) == 1
    assert len(agent1.shared_locations(agent=agent2, location_labels=[Home])) == 1
    assert len(agent1.shared_locations(agent=agent2, location_labels=[School])) == 0

    model.connect_agents(
        agents=[agent1, agent2],
        location_cls=School,
    )

    assert len(agent1.shared_locations(agent=agent2)) == 2
    assert len(agent1.shared_locations(agent=agent2, location_labels=[Home])) == 1
    assert len(agent1.shared_locations(agent=agent2, location_labels=[School])) == 1

    model.disconnect_agents(agents=[agent1, agent2], remove_locations=True)

    assert len(agent1.shared_locations(agent=agent2)) == 0
    assert len(agent1.shared_locations(agent=agent2, location_labels=[Home])) == 0
    assert len(agent1.shared_locations(agent=agent2, location_labels=[School])) == 0
