import pop2net as p2n

def test_1():
    env = p2n.Environment()
    actor1 = p2n.Actor()
    actor2 = p2n.Actor()
    location1 = p2n.Location()

    env.add_actors([actor1, actor2])
    env.add_location(location1)

    location1.add_actors([actor1, actor2])
    print(env.locations)
    assert str(env.locations) == "ObjectList [1 Elements]"
    assert repr(env.locations) == "ObjectList [1 Elements]"
    assert str(env.actors) == "ObjectList [2 Elements]"
    assert repr(env.actors) == "ObjectList [2 Elements]"

    # TODO other framework prints? 