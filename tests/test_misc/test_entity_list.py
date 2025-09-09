import pop2net as p2n

def test_print_in_environment():
    env = p2n.Environment()
    actor1 = p2n.Actor()
    actor2 = p2n.Actor()
    location1 = p2n.Location()

    env.add_actors([actor1, actor2])
    env.add_location(location1)

    location1.add_actors([actor1, actor2])
    
    assert str(env.locations) == "EntityList [1 entities]"
    assert repr(env.locations) == "EntityList [1 entities]"
    assert str(env.actors) == "EntityList [2 entities]"
    assert repr(env.actors) == "EntityList [2 entities]"


def test_print_in_creator():
    env = p2n.Environment()
    creator = p2n.Creator(env=env)
    assert str(creator.create_actors(n=10)) == "EntityList [10 entities]"