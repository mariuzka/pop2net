import pop2net as p2n


def test_agent_location_labels():
    class MyLocation(p2n.Location):
        pass

    model = p2n.Model()
    location = MyLocation(model=model)
    agent = p2n.Agent(model=model)

    agent.add_location(location)

    assert agent.location_labels == ["MyLocation"]
