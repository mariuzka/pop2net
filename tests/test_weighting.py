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

    # test agent.connect()
    model = p2n.Model()
    agent1 = p2n.Agent(model=model)
    agent2 = p2n.Agent(model=model)
    agent1.connect(agent=agent2, location_cls=p2n.Location, weight=None)
    location = model.locations[0]
    assert location.get_weight(agent=agent1) == 1
    assert location.get_weight(agent=agent2) == 1
    assert agent1.get_location_weight(location=location) == 1
    assert agent2.get_location_weight(location=location) == 1
    assert agent1.get_agent_weight(agent=agent2) == 1
    assert agent2.get_agent_weight(agent=agent1) == 1


def test_to_set_a_weight_directly():
    # test model.add_agent_to_location()
    model = p2n.Model()
    location = p2n.Location(model=model)
    agent1 = p2n.Agent(model=model)
    model.add_agent_to_location(location=location, agent=agent1, weight=77)
    assert location.get_weight(agent=agent1) == 77
    assert agent1.get_location_weight(location=location) == 77

    # test location.add_agent()
    model = p2n.Model()
    location = p2n.Location(model=model)
    agent1 = p2n.Agent(model=model)
    location.add_agent(agent=agent1, weight=77)
    assert location.get_weight(agent=agent1) == 77
    assert agent1.get_location_weight(location=location) == 77

    # test location.add_agents()
    model = p2n.Model()
    location = p2n.Location(model=model)
    agent1 = p2n.Agent(model=model)
    agent2 = p2n.Agent(model=model)
    location.add_agents(agents=[agent1, agent2], weight=77)
    assert location.get_weight(agent=agent1) == 77
    assert location.get_weight(agent=agent2) == 77
    assert agent1.get_location_weight(location=location) == 77
    assert agent2.get_location_weight(location=location) == 77
    assert agent1.get_agent_weight(agent=agent2) == 77
    assert agent2.get_agent_weight(agent=agent1) == 77

    # test location.connect_agents()
    model = p2n.Model()
    agent1 = p2n.Agent(model=model)
    agent2 = p2n.Agent(model=model)
    model.connect_agents(agents=[agent1, agent2], location_cls=p2n.Location, weight=77)
    location = model.locations[0]
    assert location.get_weight(agent=agent1) == 77
    assert location.get_weight(agent=agent2) == 77
    assert agent1.get_location_weight(location=location) == 77
    assert agent2.get_location_weight(location=location) == 77
    assert agent1.get_agent_weight(agent=agent2) == 77
    assert agent2.get_agent_weight(agent=agent1) == 77

    # test agent.connect()
    model = p2n.Model()
    agent1 = p2n.Agent(model=model)
    agent2 = p2n.Agent(model=model)
    agent1.connect(agent=agent2, location_cls=p2n.Location, weight=77)
    location = model.locations[0]
    assert location.get_weight(agent=agent1) == 77
    assert location.get_weight(agent=agent2) == 77
    assert agent1.get_location_weight(location=location) == 77
    assert agent2.get_location_weight(location=location) == 77
    assert agent1.get_agent_weight(agent=agent2) == 77
    assert agent2.get_agent_weight(agent=agent1) == 77


def test_generated_weight():
    class WeightedLocation(p2n.Location):
        def weight(self, agent):
            return 10

    # test model.add_agent_to_location()
    model = p2n.Model()
    location = WeightedLocation(model=model)
    agent1 = p2n.Agent(model=model)
    model.add_agent_to_location(location=location, agent=agent1, weight=None)
    assert location.get_weight(agent=agent1) == 10
    assert agent1.get_location_weight(location=location) == 10

    # test location.add_agent()
    model = p2n.Model()
    location = WeightedLocation(model=model)
    agent1 = p2n.Agent(model=model)
    location.add_agent(agent=agent1, weight=None)
    assert location.get_weight(agent=agent1) == 10
    assert agent1.get_location_weight(location=location) == 10

    # test location.add_agents()
    model = p2n.Model()
    location = WeightedLocation(model=model)
    agent1 = p2n.Agent(model=model)
    agent2 = p2n.Agent(model=model)
    location.add_agents(agents=[agent1, agent2], weight=None)
    assert location.get_weight(agent=agent1) == 10
    assert location.get_weight(agent=agent2) == 10
    assert agent1.get_location_weight(location=location) == 10
    assert agent2.get_location_weight(location=location) == 10
    assert agent1.get_agent_weight(agent=agent2) == 10
    assert agent2.get_agent_weight(agent=agent1) == 10

    # test location.connect_agents()
    model = p2n.Model()
    agent1 = p2n.Agent(model=model)
    agent2 = p2n.Agent(model=model)
    model.connect_agents(agents=[agent1, agent2], location_cls=WeightedLocation, weight=None)
    location = model.locations[0]
    assert location.get_weight(agent=agent1) == 10
    assert location.get_weight(agent=agent2) == 10
    assert agent1.get_location_weight(location=location) == 10
    assert agent2.get_location_weight(location=location) == 10
    assert agent1.get_agent_weight(agent=agent2) == 10
    assert agent2.get_agent_weight(agent=agent1) == 10

    # test agent.connect()
    model = p2n.Model()
    agent1 = p2n.Agent(model=model)
    agent2 = p2n.Agent(model=model)
    agent1.connect(agent=agent2, location_cls=WeightedLocation, weight=None)
    location = model.locations[0]
    assert location.get_weight(agent=agent1) == 10
    assert location.get_weight(agent=agent2) == 10
    assert agent1.get_location_weight(location=location) == 10
    assert agent2.get_location_weight(location=location) == 10
    assert agent1.get_agent_weight(agent=agent2) == 10
    assert agent2.get_agent_weight(agent=agent1) == 10


def test_individually_generated_weights():
    class WeightedLocation(p2n.Location):
        def weight(self, agent):
            return agent.w

    # test model.add_agent_to_location()
    model = p2n.Model()
    location = WeightedLocation(model=model)
    agent1 = p2n.Agent(model=model)
    agent1.w = 100
    agent2 = p2n.Agent(model=model)
    agent2.w = 200
    model.add_agent_to_location(location=location, agent=agent1, weight=None)
    model.add_agent_to_location(location=location, agent=agent2, weight=None)
    assert location.get_weight(agent=agent1) == 100
    assert agent1.get_location_weight(location=location) == 100
    assert location.get_weight(agent=agent2) == 200
    assert agent2.get_location_weight(location=location) == 200

    # test location.add_agent()
    model = p2n.Model()
    location = WeightedLocation(model=model)
    agent1 = p2n.Agent(model=model)
    agent1.w = 100
    agent2 = p2n.Agent(model=model)
    agent2.w = 200
    location.add_agent(agent=agent1, weight=None)
    location.add_agent(agent=agent2, weight=None)
    assert location.get_weight(agent=agent1) == 100
    assert agent1.get_location_weight(location=location) == 100
    assert location.get_weight(agent=agent2) == 200
    assert agent2.get_location_weight(location=location) == 200

    # test location.add_agents()
    model = p2n.Model()
    location = WeightedLocation(model=model)
    agent1 = p2n.Agent(model=model)
    agent1.w = 100
    agent2 = p2n.Agent(model=model)
    agent2.w = 200
    location.add_agents(agents=[agent1, agent2], weight=None)
    assert location.get_weight(agent=agent1) == 100
    assert agent1.get_location_weight(location=location) == 100
    assert location.get_weight(agent=agent2) == 200
    assert agent2.get_location_weight(location=location) == 200
    assert agent1.get_agent_weight(agent=agent2) == 100
    assert agent2.get_agent_weight(agent=agent1) == 100

    # test location.connect_agents()
    model = p2n.Model()
    agent1 = p2n.Agent(model=model)
    agent1.w = 100
    agent2 = p2n.Agent(model=model)
    agent2.w = 200
    model.connect_agents(agents=[agent1, agent2], location_cls=WeightedLocation, weight=None)
    location = model.locations[0]
    assert location.get_weight(agent=agent1) == 100
    assert location.get_weight(agent=agent2) == 200
    assert agent1.get_location_weight(location=location) == 100
    assert agent2.get_location_weight(location=location) == 200
    assert agent1.get_agent_weight(agent=agent2) == 100
    assert agent2.get_agent_weight(agent=agent1) == 100

    # test agent.connect()
    model = p2n.Model()
    agent1 = p2n.Agent(model=model)
    agent1.w = 100
    agent2 = p2n.Agent(model=model)
    agent2.w = 200
    agent1.connect(agent=agent2, location_cls=WeightedLocation, weight=None)
    location = model.locations[0]
    assert location.get_weight(agent=agent1) == 100
    assert location.get_weight(agent=agent2) == 200
    assert agent1.get_location_weight(location=location) == 100
    assert agent2.get_location_weight(location=location) == 200
    assert agent1.get_agent_weight(agent=agent2) == 100
    assert agent2.get_agent_weight(agent=agent1) == 100
