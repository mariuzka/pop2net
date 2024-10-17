import pop2net as p2n


def test_if_default_weight_is_1():
    # test model.add_agent_to_location()
    model = p2n.Model()
    location = p2n.Location(model=model)
    agent1 = p2n.Agent(model=model)
    model.add_agent_to_location(location=location, agent=agent1, weight=None)
    assert location.get_weight(agent=agent1) == 1
    assert agent1.get_location_weight(location=location) == 1

    # test location.add_agent()
    model = p2n.Model()
    location = p2n.Location(model=model)
    agent1 = p2n.Agent(model=model)
    location.add_agent(agent=agent1, weight=None)
    assert location.get_weight(agent=agent1) == 1
    assert agent1.get_location_weight(location=location) == 1

    # test location.add_agents()
    model = p2n.Model()
    location = p2n.Location(model=model)
    agent1 = p2n.Agent(model=model)
    agent2 = p2n.Agent(model=model)
    location.add_agents(agents=[agent1, agent2], weight=None)
    assert location.get_weight(agent=agent1) == 1
    assert location.get_weight(agent=agent2) == 1
    assert agent1.get_location_weight(location=location) == 1
    assert agent2.get_location_weight(location=location) == 1
    assert agent1.get_agent_weight(agent=agent2) == 1
    assert agent2.get_agent_weight(agent=agent1) == 1

    # test location.connect_agents()
    model = p2n.Model()
    agent1 = p2n.Agent(model=model)
    agent2 = p2n.Agent(model=model)
    model.connect_agents(agents=[agent1, agent2], location_cls=p2n.Location, weight=None)
    location = model.locations[0]
    assert location.get_weight(agent=agent1) == 1
    assert location.get_weight(agent=agent2) == 1
    assert agent1.get_location_weight(location=location) == 1
    assert agent2.get_location_weight(location=location) == 1
    assert agent1.get_agent_weight(agent=agent2) == 1
    assert agent2.get_agent_weight(agent=agent1) == 1
