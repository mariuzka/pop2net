import pop2net as p2n


def test_agent_location_labels():
    class MyLocation(p2n.Location):
        pass

    env = p2n.Environment()
    
    location = MyLocation()
    env.add_location(location)

    agent = p2n.Agent()
    env.add_agent(agent)

    agent.add_location(location)

    assert agent.location_labels == ["MyLocation"]
