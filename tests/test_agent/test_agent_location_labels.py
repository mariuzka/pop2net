import pop2net as p2n


def test_agent_location_labels():
    class MyLocation(p2n.Location):
        pass

    env = p2n.Environment()

    location = MyLocation()
    env.add_location(location)

    actor = p2n.Actor()
    env.add_actor(actor)

    actor.add_location(location)

    assert actor.location_labels == ["MyLocation"]
