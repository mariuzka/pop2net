import popy


def test_model_connect_agents_and_disconnect_agents_1():
    """A test without specifing locationt types and without removing locations from model."""

    model = popy.Model()
    agent1 = popy.Agent(model)
    agent2 = popy.Agent(model)
    agent3 = popy.Agent(model)
    agents = [agent1, agent2, agent3]

    class Home(popy.Location):
        pass

    class School(popy.Location):
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
